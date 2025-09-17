package util;

import mask.EmployeeBitMask;
import mask.EmployeeBoolFieldMask;
import model.Employee;
import model.Role;

public class EmployeeUtils {

    public static String toBoolMaskedString(Employee employee, EmployeeBoolFieldMask mask) {
        StringBuilder sb = new StringBuilder("model.Employee{");
        if (mask.id) sb.append("id=").append(employee.getId()).append(", ");
        if (mask.name) sb.append("name=").append(employee.getName()).append(", ");
        if (mask.department) sb.append("department=").append(employee.getDepartment()).append(", ");
        if (mask.workload) sb.append("workload=").append(employee.getWorkload()).append(", ");
        if (mask.role) sb.append("role=").append(employee.getRole()).append(", ");
        sb.append("}");
        return sb.toString();
    }

    public static String toBitMaskedString(Employee employee, EmployeeBitMask mask) {
        StringBuilder sb = new StringBuilder("model.Employee{");
        if (mask.has(EmployeeBitMask.ID)) sb.append("id=").append(employee.getId()).append(", ");
        if (mask.has(EmployeeBitMask.NAME)) sb.append("name=").append(employee.getName()).append(", ");
        if (mask.has(EmployeeBitMask.DEPARTMENT)) sb.append("department=").append(employee.getDepartment()).append(", ");
        if (mask.has(EmployeeBitMask.WORKLOAD)) sb.append("workload=").append(employee.getWorkload()).append(", ");
        if (mask.has(EmployeeBitMask.ROLE)) sb.append("role=").append(employee.getRole()).append(", ");
        sb.append("}");
        return sb.toString();
    }

    public static boolean equalsByMask(Employee employee1, Employee employee2, EmployeeBitMask mask) {
        if (mask.has(EmployeeBitMask.ID) && employee1.getId() != employee2.getId()) return false;
        if (mask.has(EmployeeBitMask.NAME) && !employee1.getName().equals(employee2.getName())) return false;
        if (mask.has(EmployeeBitMask.DEPARTMENT) && !employee1.getDepartment().equals(employee2.getDepartment())) return false;
        if (mask.has(EmployeeBitMask.WORKLOAD) && employee1.getWorkload() != employee2.getWorkload()) return false;
        if (mask.has(EmployeeBitMask.ROLE) && !employee1.getRole().equals(employee2.getRole())) return false;
        return true;
    }

    public static void copyFieldsByMask(Employee source, Employee target, EmployeeBitMask mask) {
        if (mask.has(EmployeeBitMask.NAME)) target.setName(source.getName());
        if (mask.has(EmployeeBitMask.DEPARTMENT)) target.setDepartment(source.getDepartment());
        if (mask.has(EmployeeBitMask.WORKLOAD)) target.setWorkload(source.getWorkload());
        if (mask.has(EmployeeBitMask.ROLE)) target.setRole(source.getRole());
    }

    public static boolean diff(Employee employee1, Employee employee2, EmployeeBitMask mask) {
        if (mask.has(EmployeeBitMask.ID) && employee1.getId() != employee2.getId()) return true;
        if (mask.has(EmployeeBitMask.NAME) && !employee1.getName().equals(employee2.getName())) return true;
        if (mask.has(EmployeeBitMask.DEPARTMENT) &&  !employee1.getDepartment().equals(employee2.getDepartment())) return true;
        if (mask.has(EmployeeBitMask.WORKLOAD) && employee1.getWorkload() != employee2.getWorkload()) return true;
        if (mask.has(EmployeeBitMask.ROLE) && !employee1.getRole().equals(employee2.getRole())) return true;
        return false;
    }

    public static boolean matchesByMask(Employee employee, EmployeeBitMask mask, Object value) {
        if (mask.has(EmployeeBitMask.ID) && value instanceof Integer) {
            return employee.getId() == (Integer) value;
        }
        if (mask.has(EmployeeBitMask.NAME) && value instanceof String) {
            return employee.getName().equals((String) value);
        }
        if (mask.has(EmployeeBitMask.DEPARTMENT) && value instanceof String) {
            return employee.getDepartment().equals((String) value);
        }
        if (mask.has(EmployeeBitMask.WORKLOAD) && value instanceof Float) {
            return employee.getWorkload() == (Float) value;
        }
        if (mask.has(EmployeeBitMask.ROLE) && value instanceof Role) {
            return employee.getRole().equals((String) value);
        }
        return false;
    }
}
