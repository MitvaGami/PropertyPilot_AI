import sqlite3
import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

# Define the path to your database file
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db', 'properties.db')

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row # This allows accessing columns by name
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

class ActionSearchProperties(Action):
    def name(self) -> Text:
        return "action_search_properties"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        location = tracker.get_slot("location")
        bhk = tracker.get_slot("bhk")
        price = tracker.get_slot("price") # This will be in Lakhs or Crores, needs normalization
        property_id = tracker.get_slot("property_id")
        amenity = tracker.get_slot("amenity")
        property_type = tracker.get_slot("property_type")

        # Basic price normalization (assuming user provides in Lakhs or Crores)
        # You might need more robust parsing for user inputs like "1.5 crore"
        min_price_lacs = 0
        max_price_lacs = float('inf') # Default to no max price

        if price is not None:
            # Simple heuristic: if number is large, assume it's in Lakhs, if small, could be Crores
            # Better would be to extract "1.5 crore" vs "150 lakhs" via NLU
            try:
                price_val = float(price)
                if price_val < 1000: # Assuming prices below 1000 are in Lakhs directly or small crores (e.g. 1.5, 2.0)
                    min_price_lacs = price_val * 0.9 # Give some flexibility
                    max_price_lacs = price_val * 1.1
                else: # Assuming user meant in lakhs directly if it's a large number
                    min_price_lacs = price_val * 0.9
                    max_price_lacs = price_val * 1.1
            except ValueError:
                print(f"Warning: Could not parse price '{price}' to a number.")
                pass # Continue without price filter

        conn = get_db_connection()
        if not conn:
            dispatcher.utter_message(text="I'm sorry, I'm having trouble connecting to the property database right now.")
            return []

        query = "SELECT property_id, location, bhk, price_lacs, amenities FROM properties WHERE status = 'Available'"
        params = []

        if property_id:
            query += " AND property_id = ?"
            params.append(property_id.upper()) # Assuming IDs are uppercase

        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")

        if bhk:
            try:
                # Extract just the number for BHK (e.g., "3BHK" -> 3)
                bhk_num = int("".join(filter(str.isdigit, bhk)))
                query += " AND bhk = ?"
                params.append(bhk_num)
            except ValueError:
                print(f"Could not parse BHK: {bhk}")

        if price is not None and min_price_lacs > 0: # Check if price was successfully processed
             query += " AND price_lacs BETWEEN ? AND ?"
             params.append(min_price_lacs)
             params.append(max_price_lacs)

        if amenity:
            query += " AND amenities LIKE ?"
            params.append(f"%{amenity}%")

        if property_type:
            # This is a very basic example; real estate types can be complex
            # You might need a more sophisticated mapping for property types
            if "villa" in property_type.lower():
                query += " AND amenities LIKE '%villa%'" # Assuming "villa" is in amenities
            elif "apartment" in property_type.lower() or "flat" in property_type.lower():
                query += " AND amenities NOT LIKE '%villa%'" # Simple negation for apartment

        print(f"Executing query: {query} with params: {params}")

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()

            if results:
                response = "Here are some properties matching your criteria:\n"
                for row in results:
                    response += (
                        f"- Property ID: {row['property_id']}, "
                        f"Location: {row['location']}, "
                        f"BHK: {row['bhk']}, "
                        f"Price: {row['price_lacs']} Lakhs, "
                        f"Amenities: {row['amenities']}.\n"
                    )
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(response="utter_no_properties_found")

        except sqlite3.Error as e:
            dispatcher.utter_message(text=f"An error occurred while searching for properties: {e}")
        finally:
            if conn:
                conn.close()

        # Clear slots after search to allow new searches without old filters
        return [SlotSet("location", None), SlotSet("bhk", None), SlotSet("price", None),
                SlotSet("property_id", None), SlotSet("amenity", None), SlotSet("property_type", None)]


class ValidatePropertyForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_property_form"

    async def extract_bhk(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:
        text = tracker.latest_message.get("text")
        bhk_extracted = None
        try:
            # Try to extract numbers from the text for BHK
            bhk_num_str = "".join(filter(str.isdigit, text))
            if bhk_num_str:
                bhk_extracted = int(bhk_num_str)
        except ValueError:
            pass # No valid integer found

        return {"bhk": bhk_extracted}

    async def validate_bhk(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate bhk value."""
        print(f"Validating bhk slot: {slot_value}")
        if slot_value and isinstance(slot_value, (int, str)):
            try:
                bhk_num = int("".join(filter(str.isdigit, str(slot_value))))
                if 1 <= bhk_num <= 6: # Assuming BHK between 1 and 6 is reasonable
                    return {"bhk": bhk_num}
                else:
                    dispatcher.utter_message(text="Please provide a valid BHK number (e.g., 1, 2, 3, 4, 5, 6).")
                    return {"bhk": None}
            except ValueError:
                dispatcher.utter_message(text="That doesn't seem like a valid BHK. Please tell me a number (e.g., 2BHK).")
                return {"bhk": None}
        else:
            dispatcher.utter_message(text="What BHK are you looking for? (e.g., 2BHK, 3 BHK)")
            return {"bhk": None}

    async def validate_price(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate price value."""
        print(f"Validating price slot: {slot_value}")
        if slot_value and isinstance(slot_value, (int, float, str)):
            try:
                # Convert common price formats like "1.5 crore" or "150 lakhs" to a numerical value
                text_lower = str(slot_value).lower()
                numeric_value = float("".join(filter(str.isdigit, text_lower.replace('.', '')))) # Remove '.' for digit check

                if "crore" in text_lower:
                    numeric_value *= 100 # Convert crores to lakhs
                elif "lac" in text_lower or "lakh" in text_lower:
                    pass # Already in lakhs
                else: # Assume direct number is in lakhs, or needs more intelligent parsing
                    if numeric_value < 10: # If user said "5", assume 5 Cr
                        numeric_value *= 100 # Convert to lakhs
                    # If user said "120", assume 120 lakhs

                if 10 <= numeric_value <= 5000: # Assuming min 10 lakhs to max 50 Crores
                    return {"price": numeric_value}
                else:
                    dispatcher.utter_message(text="Please provide a realistic budget. Prices usually range from 10 lakhs to 50 crores.")
                    return {"price": None}
            except ValueError:
                dispatcher.utter_message(text="Please provide a valid budget, for example '1.2 crore' or '90 lakhs'.")
                return {"price": None}
        else:
            dispatcher.utter_message(text="What's your approximate budget?")
            return {"price": None}

    async def validate_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate location value."""
        print(f"Validating location slot: {slot_value}")
        # In a real scenario, you'd validate against a list of known localities.
        # For now, we'll just accept any text as a valid location.
        if slot_value and isinstance(slot_value, str) and len(slot_value) > 2:
            return {"location": slot_value}
        else:
            dispatcher.utter_message(text="Which area are you looking for? Please provide a locality name.")
            return {"location": None}