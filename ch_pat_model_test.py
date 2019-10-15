import ch_pat_model
import pickle

# test_model = ch_pat_model.TestAHModel()
# test_model.store_model('test_ah_model.pkl')

test_model = pickle.load(open('test_ah_model.pkl', 'rb'))

print(test_model.model_description)
