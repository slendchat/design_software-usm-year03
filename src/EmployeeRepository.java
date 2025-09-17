import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class EmployeeRepository {
    private Map<Integer, Employee> employees = new HashMap<>();

    public void add(Employee employee) {
        employees.put(employee.getId(), employee);
    }

    public Employee findById(int id) {
        return employees.get(id);
    }

    public List<Employee> getAll() {
        return new ArrayList<Employee>(employees.values());
    }

    public void remove(int id) {
        employees.remove(id);
    }

    public List<Employee> findByName(String name) {
        List<Employee> employees = new ArrayList<>();
        EmployeeBitMask mask = new EmployeeBitMask(EmployeeBitMask.NAME);
        for (Employee employee : this.employees.values()) {
            if (EmployeeUtils.matchesByMask(employee, mask, name)) {
                employees.add(employee);
            }
        }
        return employees;
    }

    public List<Employee> findByDepartment(String department) {
        List<Employee> employees = new ArrayList<>();
        EmployeeBitMask mask = new EmployeeBitMask(EmployeeBitMask.DEPARTMENT);
        for (Employee employee : this.employees.values()) {
            if (EmployeeUtils.matchesByMask(employee, mask, department)) {
                employees.add(employee);
            }
        }
        return employees;
    }

    public List<Employee> findByWorkload(float workload) {
        List<Employee> employees = new ArrayList<>();
        EmployeeBitMask mask = new EmployeeBitMask(EmployeeBitMask.WORKLOAD);
        for (Employee employee : this.employees.values()) {
            if (EmployeeUtils.matchesByMask(employee, mask, workload)) {
                employees.add(employee);
            }
        }
        return employees;
    }

    public List<Employee> findByRole(Role role) {
        List<Employee> employees = new ArrayList<>();
        EmployeeBitMask mask = new EmployeeBitMask(EmployeeBitMask.ROLE);
        for (Employee employee : this.employees.values()) {
            if (EmployeeUtils.matchesByMask(employee, mask, role)) {
                employees.add(employee);
            }
        }
        return employees;
    }
}
