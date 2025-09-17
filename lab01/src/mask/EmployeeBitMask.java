package mask;

public class EmployeeBitMask {

    public static final int ID          = 1 << 0;
    public static final int NAME        = 1 << 1;
    public static final int DEPARTMENT  = 1 << 2;
    public static final int WORKLOAD    = 1 << 3;
    public static final int ROLE        = 1 << 4;
    public static final int ALL         = ID | NAME | DEPARTMENT | WORKLOAD | ROLE;


    private int mask;

    public EmployeeBitMask(int mask) {
        this.mask = mask;
    }
    public EmployeeBitMask() {
        this.mask = 0;
    }

    public int getMask() {
        return mask;
    }

    public void setMask(int mask) {
        this.mask = mask;
    }

    public boolean has(int field) {
        return (mask & field) != 0;
    }
}
