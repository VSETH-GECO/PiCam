import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Raspistill {
    public static int imageWidth = 1920;
    public static int imageHeight = 1080;

    public static BufferedImage getBufferedImage() {
        try {
            List<String> command = new ArrayList<String>();
            command.add("raspistill");
            //command.add("-md 1");
            command.add("-o -");

            ProcessBuilder processBuilder = new ProcessBuilder(command);
            Process process = processBuilder.start();

            return ImageIO.read(process.getInputStream());
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }

    public static BufferedImage getRawBufferedImage() {
        try {
            List<String> command = new ArrayList<String>();
            command.add("raspistillyuv");
            //command.add("-md 1");
            command.add("-rgb");
            command.add("-o -");

            ProcessBuilder processBuilder = new ProcessBuilder(command);
            Process process = processBuilder.start();

            BufferedImage image = new BufferedImage(imageWidth, imageHeight, BufferedImage.TYPE_INT_RGB);

            byte[] pixelBytes = new byte[3];
            int count = 0;
            while (process.getInputStream().read(pixelBytes) != -1) {
                int pixel = ((pixelBytes[0] << 16) + (pixelBytes[1] << 8) + (pixelBytes[2]));
                int x = count % imageWidth;
                int y = count / imageWidth;
                image.setRGB(x, y, pixel);
            }

            return image;
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }
}
