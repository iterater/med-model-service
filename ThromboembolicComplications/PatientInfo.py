class PatientInfo:
    age: int
    sex: str
    diagnosis: str

    def __init__(self, age, sex, diagnosis):
        self.age = age
        self.sex = sex
        self.diagnosis = diagnosis
