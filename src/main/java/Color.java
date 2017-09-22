/**
 * Represents a 24-bit color in RGB888 format.
 * One color actually takes up 32-bits of memory because of int.
 */
public class Color {
    private final int color;

    /**
     * Creates a new color from RGB
     *
     * @param r the red part
     * @param g the green part
     * @param b the blue part
     */
    public Color(int r, int g, int b) {
        this.color = 0xff000000 | ((r << 16) + (g << 8) + (b));
    }

    /**
     * Creates a new color from a 24-bit integer ignoring alpha channel.
     *
     * @param color the color
     */
    public Color(int color) {
        this.color = color;
    }

    /**
     * @return the color in 24-bit integer format
     */
    public int getInt() {
        return color;
    }
}
