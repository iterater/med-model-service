import json
import pickle

class ChPatModel:
    """Basic class for personalized presiction."""

    def check_applicability(self, patient_dict):
        """Check for applicability of the model against particular patient.

        Arguments:
            patient_dict {dictionary} -- Patient parameters
        """
        pass

    def apply(self, patient_dict):
        """Apply and extend the dictionary for a patient.
        
        Arguments:
            patient_dict {dictionary} -- Input dictionary for a patient            

        Returns:
            [dictionary] -- Output (extended) dictionary
        """
        return patient_dict.copy()

    def store_model(self, fname):
        pickle.dump(self, open(fname, 'wb'))

