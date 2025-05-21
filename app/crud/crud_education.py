from app.crud.base import CRUDBase
from app.models.education import (
    EducationInstitution, EducationEvent, Certification, LearningResource, LearningGoal, EducationExpense
)
from app.schemas.education import (
    EducationInstitutionCreate, EducationInstitutionInDB,
    EducationEventCreate, EducationEventInDB,
    CertificationCreate, CertificationInDB,
    LearningResourceCreate, LearningResourceInDB,
    LearningGoalCreate, LearningGoalInDB,
    EducationExpenseCreate, EducationExpenseInDB
)

education_institution = CRUDBase[EducationInstitution, EducationInstitutionCreate, EducationInstitutionInDB](EducationInstitution)
education_event = CRUDBase[EducationEvent, EducationEventCreate, EducationEventInDB](EducationEvent)
certification = CRUDBase[Certification, CertificationCreate, CertificationInDB](Certification)
learning_resource = CRUDBase[LearningResource, LearningResourceCreate, LearningResourceInDB](LearningResource)
learning_goal = CRUDBase[LearningGoal, LearningGoalCreate, LearningGoalInDB](LearningGoal)
education_expense = CRUDBase[EducationExpense, EducationExpenseCreate, EducationExpenseInDB](EducationExpense) 