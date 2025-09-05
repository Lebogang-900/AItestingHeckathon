namespace AcademicSystem.Data;

public class StudentService
{
    private List<Student> Students = new();
    private int _counter = 1;

    public List<Student> GetStudents() => Students;

    public void AddStudent(string name, string email)
    {
        Students.Add(new Student { Id = _counter++, Name = name, Email = email });
    }
}
