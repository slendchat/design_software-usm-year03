import mask.EmployeeBitMask;
import mask.EmployeeBoolFieldMask;
import model.Employee;
import model.Role;
import repository.EmployeeRepository;
import util.EmployeeUtils;

public class Main
{
    public static void main(String[] args) {
        EmployeeRepository repo = new EmployeeRepository();

        Employee employee   = new Employee("Jhon Doe", "IT",0.75f, Role.MIDDLE);
        Employee employee2  = new Employee("Alfredo Mustacho", "INFRA",0.75f, Role.SENIOR);
        Employee employee3  = new Employee("Artur Dexter", "IT",0.87f, Role.MIDDLE);
        Employee employee4  = new Employee("Jhon Doe", "INFRA",0.55f, Role.TEAMLEAD);

        repo.add(employee);
        repo.add(employee2);
        repo.add(employee3);
        repo.add(employee4);

        EmployeeBoolFieldMask boolMask = new EmployeeBoolFieldMask(false,true, true, false,true);
        EmployeeBitMask bitMask = new EmployeeBitMask();
        bitMask.setMask(EmployeeBitMask.NAME | EmployeeBitMask.ROLE);

        System.out.println("=== Output with bool-mask ===");
        System.out.println(EmployeeUtils.toBoolMaskedString(employee,boolMask));
        System.out.println(EmployeeUtils.toBoolMaskedString(employee,EmployeeBoolFieldMask.BASIC));

        System.out.println("\n=== Output with bit-mask ===");
        System.out.println(EmployeeUtils.toBitMaskedString(employee,bitMask));

        System.out.println("\n=== Find by name ===");
        System.out.println(repo.findByName("Alfredo Mustacho"));

        System.out.println("\n=== equalsByMask ===");
        EmployeeBitMask eqMask = new EmployeeBitMask(EmployeeBitMask.DEPARTMENT | EmployeeBitMask.ROLE);
        System.out.println("employee1 and employee3 equal by department+role: " +
                EmployeeUtils.equalsByMask(employee, employee3, eqMask));
        System.out.println("employee1 and employee2 equal by department+role: " +
                EmployeeUtils.equalsByMask(employee, employee3, eqMask));

        System.out.println("\n=== copyFieldsByMask ===");
        EmployeeBitMask copyMask = new EmployeeBitMask(EmployeeBitMask.DEPARTMENT);
        EmployeeUtils.copyFieldsByMask(employee2, employee, copyMask);
        System.out.println("After copying: " +
                EmployeeUtils.toBitMaskedString(employee, new EmployeeBitMask(EmployeeBitMask.ALL)));

        System.out.println("\n=== diff ===");
        System.out.println("Are employee1 and employee3 different by name? " +
                EmployeeUtils.diff(employee, employee3, new EmployeeBitMask(EmployeeBitMask.NAME)));

        System.out.println("\n=== matchesByMask ===");
        System.out.println("employee2 name == Bob ? " +
                EmployeeUtils.matchesByMask(employee2, new EmployeeBitMask(EmployeeBitMask.NAME), "Bob"));
        System.out.println("employee2 workload == 0.75 ? " +
                EmployeeUtils.matchesByMask(employee2, new EmployeeBitMask(EmployeeBitMask.WORKLOAD), 0.75f));

    }
}