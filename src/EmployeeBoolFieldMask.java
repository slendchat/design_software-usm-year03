public final class EmployeeBoolFieldMask {
    public boolean id;
    public boolean name;
    public boolean department;
    public boolean workload;
    public boolean role;

    public static final EmployeeBoolFieldMask ALL = new EmployeeBoolFieldMask(true, true, true, true, true);
    public static final EmployeeBoolFieldMask BASIC = new EmployeeBoolFieldMask(true, true, true, false, false);

    /**
     * Конструктор со всеми параметрами.
     *
     * @param id unique id mask
     * @param name employee name mask
     * @param workload employee workload mask
     * @param role employee role mask
     */
    EmployeeBoolFieldMask(boolean id, boolean name, boolean department, boolean workload, boolean role) {
        this.id = id;
        this.name = name;
        this.department = department;
        this.workload = workload;
        this.role = role;
    }

}
