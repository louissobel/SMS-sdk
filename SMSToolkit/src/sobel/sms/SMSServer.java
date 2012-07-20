package sobel.sms;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

import android.util.Log;

public class SMSServer extends Thread {

	private ServerSocket serverSocket;
	private SMSToolkitActivity activity;

	private static final String TAG = "SMSServer";
	
	public SMSServer(SMSToolkitActivity a,  int port) throws IOException {

		activity = a;
		serverSocket = new ServerSocket(port);
		
		LogAction logger = new LogAction(
				String.format(
					"SMSServer listening on port %d",
					port
				),
				activity	
			);
		activity.runOnUiThread(logger);

	}

	@Override
	public void run() {

		while (true) {
			try {
				Socket connection = serverSocket.accept();
				
				Log.d(TAG, "Connection made...");

				// should only have one connection open at a time
				SMSSender sender = new SMSSender(activity, connection);
				SMSRelayer relayer = new SMSRelayer(activity, connection);
				sender.start();
				relayer.start();
						
				
				LogAction logger = new LogAction(
					String.format(
						"connected to %s", 
						connection.getInetAddress().toString()
					),
					activity	
				);
				activity.runOnUiThread(logger);
				
				

			} catch (IOException e) {
				e.printStackTrace();
				// but leave the serveSocket open!
			}

		}

	}

}
