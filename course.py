class Course:
    def __init__(self, name, code, units, description, prerequisites=None):
        self.name = name
        self.code = code
        self.units = units
        self.description = description
        self.prerequisites = prerequisites

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "units": self.units,
            "description": self.description,
            "prerequisites": self.prerequisites
        }
    
courses = {
    
}  

graph = {

}