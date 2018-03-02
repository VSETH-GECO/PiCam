import com.hopding.jrpicam.RPiCamera;

import java.io.IOException;
import java.util.TimerTask;

class PictureTaker extends TimerTask {
    RPiCamera piCam;
    int picNum;

    PictureTaker(RPiCamera piCam) {
        this.piCam = piCam;
        this.picNum = 1;
    }

    public void run() {
        try {
            piCam.takeStill(String.format("%010d", picNum) + ".jpg");
            picNum++;

        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}