from django.db import models
from django.contrib.auth.models import User # use the built-in User model for authentication
"""
For reference:
Django's built-in User model includes:
Username
Password
Email
First and last name
Administrative flags (is_staff, is_active, etc.)
Authentication methods

Example usage:
user = User.objects.get(username='student1')
full_name = f"{user.first_name} {user.last_name}"
"""
from collections import namedtuple


# Define the grade scale once as a constant to avoid recreating it on each function call
GradeValue = namedtuple('GradeValue', ['letter', 'points', 'min_percentage', 'max_percentage'])
GLASGOW_GRADE_SCALE = [
    GradeValue('A1', 22, 92, 100),
    GradeValue('A2', 21, 85, 91),
    GradeValue('A3', 20, 79, 84),
    GradeValue('A4', 19, 74, 78),
    GradeValue('A5', 18, 70, 73),
    GradeValue('B1', 17, 67, 69),
    GradeValue('B2', 16, 64, 66),
    GradeValue('B3', 15, 60, 63),
    GradeValue('C1', 14, 57, 59),
    GradeValue('C2', 13, 54, 56),
    GradeValue('C3', 12, 50, 53),
    GradeValue('D1', 11, 47, 49),
    GradeValue('D2', 10, 44, 46),
    GradeValue('D3', 9, 40, 43),
    GradeValue('E1', 8, 37, 39),
    GradeValue('E2', 7, 34, 36),
    GradeValue('E3', 6, 30, 33),
    GradeValue('F1', 5, 27, 29),
    GradeValue('F2', 4, 24, 26),
    GradeValue('F3', 3, 20, 23),
    GradeValue('G1', 2, 15, 19),
    GradeValue('G2', 1, 10, 14),
    GradeValue('H', 0, 0, 9)
]
"""
Example usage of GradeValue objects:
grade_obj = GLASGOW_GRADE_SCALE[0]  # Gets A1 grade
letter = grade_obj.letter  # 'A1'
points = grade_obj.points  # 22
min_perc = grade_obj.min_percentage  # 92
max_perc = grade_obj.max_percentage  # 100

# In templates:
# {{ grade_obj.letter }} - {{ grade_obj.points }} points
"""

class Course(models.Model):
    """
    Course model representing academic courses a student is taking.
    Each course belongs to a specific user and can have multiple assignments.
    
    Example usage:
    # Create a new course
    new_course = Course(user=request.user, course_name="Mathematics", credit_hours=4.0)
    new_course.save()
    
    # Get all courses for a user
    user_courses = Course.objects.filter(user=request.user)
    
    # Calculate course grade
    grade = course.calculate_overall_grade()
    if grade is not None:
        grade_obj = convert_to_gpa_scale(grade)
        letter_grade = grade_obj.letter
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    course_name = models.CharField(max_length=50)
    credit_hours = models.DecimalField(max_digits=3, decimal_places=1, default=3.0)
    
    def __str__(self):
        return self.course_name
    
    def get_graded_assignments(self):
        return self.assignments.filter(graded=True, grade__isnull=False)
    
    def get_manual_grades(self):
        """
        Get all manually added grades for the course.
        """
        return self.grades.filter(is_manual=True)
    
    def calculate_course_grade(self):
        """
        Calculate the grade for the course based on the grades of the assignments.
        """
        assignments = self.get_graded_assignments()
        if not assignments:
            return None
        total_weight = sum([assignment.weight for assignment in assignments])
        if total_weight == 0:
            return None
        weighted_grades = sum([assignment.grade.grade * assignment.weight for assignment in assignments])
        return weighted_grades / total_weight
    
    
    def calculate_overall_grade(self):
        """Calculate the overall grade for the course, including manual grades."""
        assignment_grades = self.get_graded_assignments()
        manual_grades = self.get_manual_grades()

        if not assignment_grades and not manual_grades:
            return None
        
        total_weight = sum([assignment.weight for assignment in assignment_grades]) + sum([grade.weight for grade in manual_grades])
        
        if total_weight == 0: #in case user enters 0 weight for all manual grades and has no assignements
            return None
        
        weighted_grades = sum([assignment.grade.grade * assignment.weight for assignment in assignment_grades])
        manual_weighted_grades = sum([grade.grade * grade.weight for grade in manual_grades])

        return (weighted_grades + manual_weighted_grades) / total_weight

class Grade(models.Model):
    """
    Grade model representing a grade received for an assignment or manually added.
    Each grade belongs to a user and has optional notes.
    
    Example usage:
    # Creating a manual grade
    from django.utils import timezone

    #ONLY IF USER IS LOGGED IN:
    manual_grade = Grade(
        user=request.user, 
        course=course,
        grade=85.5,
        weight=0.4,
        date=timezone.now(),
        note="Midterm exam",
        is_manual=True
    )
    manual_grade.save()


    # Get all grades for a user
    user_grades = Grade.objects.filter(user=request.user)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades', null=True, blank=True)
    grade = models.FloatField()
    weight = models.FloatField(default=1.0)
    date = models.DateTimeField()
    note = models.CharField(max_length=256, blank=True)
    is_manual = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.grade} - {self.date.strftime('%Y-%m-%d')}"


class Assignment(models.Model):
    """
    Assignment model representing academic tasks with deadlines.
    Each assignment belongs to a course and may have an associated grade.
    
    Example usage:
    # Create new assignment
    from django.utils import timezone
    new_assignment = Assignment(
        course=course,
        deadline=timezone.now() + timezone.timedelta(days=7),
        name="Term Paper",
        weight=0.3,
        note="8-10 pages"
    )
    new_assignment.save()
    
    # Add grade to existing assignment
    assignment.grade = Grade(...)
    assignment.graded = True
    assignment.save()
    
    # Get upcoming assignments
    upcoming = Assignment.objects.filter(deadline__gte=timezone.now()).order_by('deadline')
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    grade = models.OneToOneField(Grade, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignment')
    graded = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    name = models.CharField(max_length=25)
    weight = models.FloatField(default=1.0)
    note = models.CharField(max_length=256, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['deadline']

def calculate_overall_gpa(user):
    """
    Calculate overall GPA weighted by credit hours for a user
    
    # Calculate overall GPA for a user
    user_gpa = calculate_overall_gpa(request.user)
    if user_gpa is not None:
        gpa_object = convert_to_gpa_scale(user_gpa)
    letter_grade = gpa_object.letter
    points = gpa_object.points
    """
    courses = user.courses.all()
    if not courses:
        return None
        
    total_credits = 0
    weighted_sum = 0
    
    for course in courses:
        course_grade = course.calculate_overall_grade()
        if course_grade is not None:
            course_credits = float(course.credit_hours)
            weighted_sum += course_grade * course_credits
            total_credits += course_credits
            
    if total_credits == 0:
        return None
            
    return weighted_sum / total_credits


def convert_to_gpa_scale(percentage_grade):
    """
    Convert percentage grade to Glasgow University's 22-point scale
    Returns a GradeValue object with letter grade, point value, and percentage range
    
    Reference: https://www.gla.ac.uk/media/Media_124293_smxx.pdf
    
    # Convert a percentage grade to Glasgow scale
    grade_obj = convert_to_gpa_scale(87.5)  # Returns A2 GradeValue object
    letter = grade_obj.letter  # 'A2'
    points = grade_obj.points  # 21

    # In templates:
    {{ grade_obj.letter }} ({{ grade_obj.points }} points)
    """
    if percentage_grade is None:
        return None
        
    for grade in GLASGOW_GRADE_SCALE:
        if grade.min_percentage <= percentage_grade <= grade.max_percentage:
            return grade
            
    return None  # Should never reach here, security measure

class TempCourse:
    """
    Temporary course class for GPA calculations without database persistence.
    Used for unregistered users who want to calculate GPA without logging in.
    
    Example usage:
    # Create temporary courses
    math = TempCourse("Mathematics", 4.0, [85, 92, 78], [0.3, 0.4, 0.3])
    physics = TempCourse("Physics", 3.0, [75, 82], [0.5, 0.5])
    
    # Calculate GPA
    courses = [math, physics]
    gpa = calculate_gpa_for_temp_courses(courses)
    grade_obj = convert_to_gpa_scale(gpa)
    """
    def __init__(self, name, credit_hours, grades, weights=None):
        self.name = name
        self.credit_hours = float(credit_hours)
        self.grades = grades
        
        # If weights aren't provided, distribute weight equally
        if weights is None:
            count = len(grades)
            self.weights = [1.0/count] * count if count > 0 else []
        else:
            # Normalize weights to sum to 1.0
            total = sum(weights)
            self.weights = [w/total for w in weights] if total > 0 else []
            
    def calculate_grade(self):
        """Calculate the weighted average grade for this temporary course"""
        if not self.grades or len(self.grades) == 0:
            return None
            
        if len(self.grades) != len(self.weights):
            raise ValueError("Number of grades must match number of weights")
            
        weighted_sum = sum(g * w for g, w in zip(self.grades, self.weights))
        return weighted_sum


def calculate_gpa_for_temp_courses(temp_courses):
    """
    Calculate GPA for a list of temporary courses without database persistence.
    
    Example usage:
    # For unregistered users:
    courses = [
        TempCourse("Math", 4.0, [90, 85, 95], [0.3, 0.3, 0.4]),
        TempCourse("Physics", 3.0, [80, 75], [0.5, 0.5])
    ]
    gpa = calculate_gpa_for_temp_courses(courses)
    grade_obj = convert_to_gpa_scale(gpa)
    """
    if not temp_courses:
        return None
        
    total_credits = 0
    weighted_sum = 0
    
    for course in temp_courses:
        course_grade = course.calculate_grade()
        if course_grade is not None:
            weighted_sum += course_grade * course.credit_hours
            total_credits += course.credit_hours
            
    if total_credits == 0:
        return None
            
    return weighted_sum / total_credits