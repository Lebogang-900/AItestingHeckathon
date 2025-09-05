namespace AcademicSystem.Data;

public class Student
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
}

public class Course
{
    public int Id { get; set; }
    public string Title { get; set; } = "";
}
