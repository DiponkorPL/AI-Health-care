public class Student {
    private String id;
    private String name;
    private String department;

    public Student(String id, String name, String department) {
        this.id = id;
        this.name = name;
        this.department = department;
    }

    public String getId() { return id; }
    public String getInfo() {
        return "ID: " + id + " | Name: " + name + " | Dept: " + department;
    }
}
