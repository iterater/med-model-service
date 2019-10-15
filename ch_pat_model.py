import json
import pickle

class ChPatModel:
    """Basic class for personalized presiction."""

    def check_applicability(self, patient_dict):
        """Check for applicability of the model against particular patient described in patient_dict."""
        pass

    def apply(self, patient_dict):
        """Apply and extend the dictionary for a patient (patient_dict)."""
        return patient_dict.copy()

    def store_model(self, fname):
        """Store the model in pickle file"""
        pickle.dump(self, open(fname, 'wb'))

