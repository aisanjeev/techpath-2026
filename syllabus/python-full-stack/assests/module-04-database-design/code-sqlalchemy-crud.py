"""
Module 04: SQLAlchemy ORM CRUD Operations
TechPath Institute - Python Full Stack Course

This script demonstrates:
- Defining SQLAlchemy models with relationships
- Creating tables automatically
- CRUD operations (Create, Read, Update, Delete)
- Relationship queries and eager loading
- Filtering, ordering, and aggregation

Requirements:
    pip install sqlalchemy
"""

from datetime import datetime, date
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean,
    Date, DateTime, ForeignKey, Text, func, and_, or_
)
from sqlalchemy.orm import (
    declarative_base, relationship, sessionmaker, joinedload
)

# ==============================================================
# 1. DEFINE MODELS
# ==============================================================

Base = declarative_base()


class Course(Base):
    """A course offered by TechPath Institute."""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    duration_months = Column(Integer, nullable=False)
    fee = Column(Float, nullable=False)
    category = Column(String(50), default="Technical")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # One course has many enrollments
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(id={self.id}, name='{self.name}', fee={self.fee})>"


class Student(Base):
    """A student at TechPath Institute."""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(15))
    city = Column(String(50), default="Bhopal")
    is_active = Column(Boolean, default=True)
    enrolled_date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.utcnow)

    # One student has many enrollments
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', city='{self.city}')>"


class Enrollment(Base):
    """Links students to courses (many-to-many through this table)."""
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_date = Column(Date, default=date.today)
    status = Column(String(20), default="active")  # active, completed, dropped
    grade = Column(String(2))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment(student_id={self.student_id}, course_id={self.course_id}, status='{self.status}')>"


# ==============================================================
# 2. DATABASE SETUP
# ==============================================================

def setup_database():
    """Create the database engine and tables."""
    # Using SQLite for simplicity (no server needed)
    engine = create_engine("sqlite:///techpath.db", echo=False)

    # Create all tables defined by our models
    Base.metadata.create_all(engine)
    print("Database and tables created successfully!")

    # Create a session factory
    Session = sessionmaker(bind=engine)
    return Session()


# ==============================================================
# 3. CREATE -- Insert Data
# ==============================================================

def seed_data(session):
    """Insert sample data into the database."""

    # Check if data already exists
    if session.query(Course).count() > 0:
        print("Data already exists, skipping seed.")
        return

    # --- Create Courses ---
    courses = [
        Course(name="Python Full Stack", duration_months=6, fee=35000, category="Development"),
        Course(name="Data Science with Python", duration_months=4, fee=28000, category="Data"),
        Course(name="Java Full Stack", duration_months=6, fee=32000, category="Development"),
        Course(name="Web Development", duration_months=3, fee=18000, category="Development"),
        Course(name="DevOps & Cloud", duration_months=4, fee=30000, category="Infrastructure"),
    ]
    session.add_all(courses)
    session.flush()  # Get IDs without committing
    print(f"Inserted {len(courses)} courses.")

    # --- Create Students ---
    students = [
        Student(name="Rahul Sharma", email="rahul@techpath.in", phone="9876543210", city="Bhopal"),
        Student(name="Priya Patel", email="priya@techpath.in", phone="9876543211", city="Pune"),
        Student(name="Amit Kumar", email="amit@techpath.in", phone="9876543212", city="Delhi"),
        Student(name="Sneha Gupta", email="sneha@techpath.in", phone="9876543213", city="Indore"),
        Student(name="Vikram Singh", email="vikram@techpath.in", phone="9876543214", city="Hyderabad"),
        Student(name="Ananya Reddy", email="ananya@techpath.in", phone="9876543215", city="Bhopal"),
        Student(name="Karan Mehta", email="karan@techpath.in", phone="9876543216", city="Delhi"),
        Student(name="Neha Joshi", email="neha@techpath.in", phone="9876543217", city="Pune"),
    ]
    session.add_all(students)
    session.flush()
    print(f"Inserted {len(students)} students.")

    # --- Create Enrollments ---
    enrollments = [
        Enrollment(student_id=1, course_id=1, status="active"),      # Rahul -> Python
        Enrollment(student_id=2, course_id=1, status="active"),      # Priya -> Python
        Enrollment(student_id=3, course_id=3, status="active"),      # Amit -> Java
        Enrollment(student_id=4, course_id=2, status="completed", grade="A"),  # Sneha -> Data Science
        Enrollment(student_id=5, course_id=1, status="active"),      # Vikram -> Python
        Enrollment(student_id=6, course_id=4, status="completed", grade="B"),  # Ananya -> Web Dev
        Enrollment(student_id=7, course_id=5, status="active"),      # Karan -> DevOps
        Enrollment(student_id=8, course_id=2, status="active"),      # Neha -> Data Science
        Enrollment(student_id=1, course_id=2, status="active"),      # Rahul also in Data Science
    ]
    session.add_all(enrollments)
    session.commit()
    print(f"Inserted {len(enrollments)} enrollments.")
    print("-" * 50)


# ==============================================================
# 4. READ -- Query Data
# ==============================================================

def read_all_students(session):
    """Fetch and display all students."""
    print("\n=== All Students ===")
    students = session.query(Student).order_by(Student.name).all()
    print(f"{'ID':<4} {'Name':<20} {'Email':<25} {'City':<12} {'Active'}")
    print("-" * 70)
    for s in students:
        print(f"{s.id:<4} {s.name:<20} {s.email:<25} {s.city:<12} {s.is_active}")
    print(f"\nTotal: {len(students)} students")


def read_students_by_city(session, city):
    """Find students from a specific city."""
    print(f"\n=== Students from {city} ===")
    students = session.query(Student).filter_by(city=city).all()
    for s in students:
        print(f"  - {s.name} ({s.email})")
    print(f"Total: {len(students)}")


def read_with_filters(session):
    """Demonstrate various filtering options."""
    print("\n=== Filtered Queries ===")

    # Active students from Bhopal or Delhi
    results = session.query(Student).filter(
        Student.is_active == True,
        Student.city.in_(["Bhopal", "Delhi"])
    ).all()
    print(f"\nActive students from Bhopal or Delhi: {len(results)}")
    for s in results:
        print(f"  - {s.name} ({s.city})")

    # Students whose name contains 'a' (case insensitive)
    results = session.query(Student).filter(
        Student.name.ilike("%a%")
    ).order_by(Student.name).all()
    print(f"\nStudents with 'a' in name: {len(results)}")
    for s in results:
        print(f"  - {s.name}")

    # Count students per city
    city_counts = session.query(
        Student.city,
        func.count(Student.id).label("total")
    ).group_by(Student.city).order_by(func.count(Student.id).desc()).all()
    print("\nStudents per city:")
    for city, total in city_counts:
        print(f"  {city}: {total}")


def read_all_courses(session):
    """Fetch and display all courses."""
    print("\n=== All Courses ===")
    courses = session.query(Course).order_by(Course.fee.desc()).all()
    print(f"{'ID':<4} {'Course':<25} {'Duration':<12} {'Fee':>10} {'Category'}")
    print("-" * 65)
    for c in courses:
        print(f"{c.id:<4} {c.name:<25} {c.duration_months:<12} Rs. {c.fee:>7,.0f} {c.category}")


# ==============================================================
# 5. RELATIONSHIP QUERIES
# ==============================================================

def read_with_relationships(session):
    """Query data across related tables using relationships."""
    print("\n=== Student Enrollments (Relationship Queries) ===")

    # Eager load students with their enrollments and courses
    students = session.query(Student).options(
        joinedload(Student.enrollments).joinedload(Enrollment.course)
    ).all()

    for student in students:
        if student.enrollments:
            print(f"\n{student.name} ({student.city}):")
            for enrollment in student.enrollments:
                status_icon = "Active" if enrollment.status == "active" else "Done"
                grade_str = f" (Grade: {enrollment.grade})" if enrollment.grade else ""
                print(f"  -> {enrollment.course.name} [{status_icon}]{grade_str}")
        else:
            print(f"\n{student.name} ({student.city}): No enrollments")


def read_course_students(session):
    """For each course, show enrolled students."""
    print("\n=== Course-wise Student List ===")

    courses = session.query(Course).options(
        joinedload(Course.enrollments).joinedload(Enrollment.student)
    ).all()

    for course in courses:
        active_enrollments = [e for e in course.enrollments if e.status == "active"]
        print(f"\n{course.name} (Rs. {course.fee:,.0f}) - {len(active_enrollments)} active students:")
        for enrollment in course.enrollments:
            status = f"[{enrollment.status}]"
            print(f"  - {enrollment.student.name} from {enrollment.student.city} {status}")


# ==============================================================
# 6. UPDATE -- Modify Data
# ==============================================================

def update_student(session):
    """Update a student's information."""
    print("\n=== Update Student ===")

    # Find Rahul
    student = session.query(Student).filter_by(email="rahul@techpath.in").first()
    if student:
        print(f"Before: {student.name}, City: {student.city}, Phone: {student.phone}")

        # Update city and phone
        student.city = "Hyderabad"
        student.phone = "9988776655"
        session.commit()

        print(f"After:  {student.name}, City: {student.city}, Phone: {student.phone}")
        print("Student updated successfully!")
    else:
        print("Student not found.")


def update_enrollment_status(session):
    """Mark an enrollment as completed with a grade."""
    print("\n=== Update Enrollment Status ===")

    # Find Amit's Java enrollment
    enrollment = session.query(Enrollment).join(Student).join(Course).filter(
        Student.name == "Amit Kumar",
        Course.name == "Java Full Stack"
    ).first()

    if enrollment:
        print(f"Before: {enrollment.student.name} - {enrollment.course.name} [{enrollment.status}]")
        enrollment.status = "completed"
        enrollment.grade = "A"
        session.commit()
        print(f"After:  {enrollment.student.name} - {enrollment.course.name} [{enrollment.status}] Grade: {enrollment.grade}")
    else:
        print("Enrollment not found.")


# ==============================================================
# 7. DELETE -- Remove Data
# ==============================================================

def delete_student(session):
    """Delete a student and their enrollments (cascade)."""
    print("\n=== Delete Student ===")

    # Count before
    count_before = session.query(Student).count()

    # Find and delete Karan
    student = session.query(Student).filter_by(name="Karan Mehta").first()
    if student:
        print(f"Deleting: {student.name} ({student.email})")
        session.delete(student)  # Cascade deletes enrollments too
        session.commit()

        count_after = session.query(Student).count()
        print(f"Students before: {count_before}, after: {count_after}")
        print("Student and related enrollments deleted successfully!")
    else:
        print("Student not found (may have been deleted already).")


# ==============================================================
# 8. AGGREGATION QUERIES
# ==============================================================

def aggregation_queries(session):
    """Demonstrate aggregate functions with SQLAlchemy."""
    print("\n=== Aggregation Queries ===")

    # Total students
    total = session.query(func.count(Student.id)).scalar()
    print(f"Total students: {total}")

    # Average course fee
    avg_fee = session.query(func.avg(Course.fee)).scalar()
    print(f"Average course fee: Rs. {avg_fee:,.0f}")

    # Most expensive course
    max_course = session.query(Course).order_by(Course.fee.desc()).first()
    print(f"Most expensive course: {max_course.name} (Rs. {max_course.fee:,.0f})")

    # Students per city
    print("\nStudents per city:")
    city_stats = session.query(
        Student.city,
        func.count(Student.id).label("count")
    ).group_by(Student.city).order_by(func.count(Student.id).desc()).all()

    for city, count in city_stats:
        print(f"  {city}: {count}")

    # Enrollments per course
    print("\nEnrollments per course:")
    course_stats = session.query(
        Course.name,
        func.count(Enrollment.id).label("enrollments")
    ).outerjoin(Enrollment).group_by(Course.name).order_by(
        func.count(Enrollment.id).desc()
    ).all()

    for name, count in course_stats:
        print(f"  {name}: {count} enrollments")


# ==============================================================
# MAIN -- Run everything
# ==============================================================

def main():
    print("=" * 60)
    print("  TechPath Institute - SQLAlchemy CRUD Demo")
    print("=" * 60)

    # Setup
    session = setup_database()

    # CREATE
    seed_data(session)

    # READ
    read_all_courses(session)
    read_all_students(session)
    read_students_by_city(session, "Bhopal")
    read_with_filters(session)

    # RELATIONSHIPS
    read_with_relationships(session)
    read_course_students(session)

    # AGGREGATION
    aggregation_queries(session)

    # UPDATE
    update_student(session)
    update_enrollment_status(session)

    # DELETE
    delete_student(session)

    # Final state
    print("\n" + "=" * 60)
    print("  Final State After All Operations")
    print("=" * 60)
    read_all_students(session)

    # Cleanup
    session.close()
    print("\nDone! Check techpath.db for the database file.")


if __name__ == "__main__":
    main()
