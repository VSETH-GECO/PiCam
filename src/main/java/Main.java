import com.hopding.jrpicam.RPiCamera;
import com.hopding.jrpicam.enums.Encoding;
import com.hopding.jrpicam.enums.Exposure;
import com.hopding.jrpicam.exceptions.FailedToRunRaspistillException;

import java.io.IOException;

/**
 * Sets up a rasperry pi camera and starts a timer to take
 * a picture in a defined interval.
 */
public class Main {
    // Interval in which to take the pictures
    private static int captureInterval = 5000;

    public static void main(String[] args) {
        while (true) {
            try {
                RPiCamera piCamera = new RPiCamera("/home/pi/nfs/pi-cam");

                piCamera.setWidth(1920).setHeight(1080)
                        .setExposure(Exposure.AUTO);

                piCamera.setEncoding(Encoding.PNG)
                        .setTimeout(10000);

                System.out.println("Setup complete; Starting timelapse...");
                piCamera.timelapse(true, "%04d_timelapse.png", captureInterval);

            } catch (FailedToRunRaspistillException | IOException | InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
