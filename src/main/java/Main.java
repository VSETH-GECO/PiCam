import com.hopding.jrpicam.RPiCamera;
import com.hopding.jrpicam.enums.Exposure;
import com.hopding.jrpicam.exceptions.FailedToRunRaspistillException;

import java.util.Timer;

/**
 * Idea: 
 * Captures images in a given interval and processes them to a video using ffmpeg.
 */
public class Main {
    static int captureInterval = 1000;

    public static void main(String[] args) {
        try {
            RPiCamera piCamera = new RPiCamera("/home/pi/Pictures");

            piCamera.setWidth(1920).setHeight(1080)
                    .setBrightness(75)
                    .setExposure(Exposure.AUTO);

            PictureTaker picTaker = new PictureTaker(piCamera);
            Timer timer = new Timer();

            timer.schedule(picTaker, 1000, captureInterval);

        } catch (FailedToRunRaspistillException e) {
            e.printStackTrace();
        }


    }
}
