package sobel.sms;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

public class SMSToolkitActivity extends Activity {
	/** Called when the activity is first created. */

	private static final String TAG = "SMSToolkit";

	private TextView logText;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);

		logText = (TextView) findViewById(R.id.log);
		log("HELLO");
		log("whatsup");
		
		SMSServer server = null;
		try {
			server = new SMSServer(this, 7801);
			Log.d(TAG, "Server created OK");
		} catch (IOException e) {
			Log.e(TAG, "Error creating server");
		}

		if (server != null) {
			server.start();
		}

	}
	
	public void log(String message) {
		Date now = new Date();
		SimpleDateFormat logFormatter = new SimpleDateFormat("MM dd HH:mm");
		String timeStamp = logFormatter.format(now);
		
		logText.append(String.format("[%s] - %s\n", timeStamp, message));
		
	}
	
	public void logSend(TextMessage t) {
		String message = String.format("sent message to %s", t.to);
		log(message);
	}
	
	public void logReceive(TextMessage t) {
		String message = String.format("received message from %s", t.from);
		log(message);
	}
}