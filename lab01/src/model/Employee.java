package model;

//Domain model class
public final class Employee {
    //primitive id auto apply
    private static int idCounter = 0;
    private int id;
    private String name;
    private String Department;
    private float workload;
    private Role role;
    public Employee(String name, String department, float workload, Role role) {
        this.id = ++idCounter;
        this.name = name;
        this.Department = department;
        this.workload = workload;
        this.role = role;
    }

    public int getId() {return id;}
    public String getName() {return name;}
    public String getDepartment() {return Department;}
    public float getWorkload() {return workload;}
    public Role getRole() {return role;}
    public void setName(String name) {this.name = name;}
    public void setDepartment(String Department) {this.Department = Department;}
    public void setWorkload(float workload) {this.workload = workload;}
    public void setRole(Role role) {this.role = role;}

    @Override
    public String toString() {
        return "model.Employee{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", department='" + Department + '\'' +
                ", workload=" + workload +
                ", role=" + role +
                '}';
    }
}



