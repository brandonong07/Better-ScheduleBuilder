class Course:
    def __init__(self, name, code, units, description):
        self.name = name
        self.code = code
        self.units = units
        self.description = description

courses = {
    
}  

graph = {

}

'''
sta32 = Course("Gateway to Statistical Data Science", "STA32", 4, "An introduction to statistical data science, covering data manipulation, visualization, and basic statistical analysis.")
sta106 = Course("Analysis of Variance", "STA106", 4, "A course on analysis of variance (ANOVA), including one-way and two-way ANOVA, as well as post-hoc tests.")
sta108 = Course("Regression Analysis", "STA108", 4, "A course on regression analysis, including linear regression, logistic regression, and model evaluation techniques.")
  
courses["STA 032"] = sta32
courses["STA 106"] = sta106
courses["STA 108"] = sta108

graph["STA 108"] = set()
graph["STA 108"].add("STA 032")

print(graph["STA 108"])
'''