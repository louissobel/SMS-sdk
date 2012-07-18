package sobel.sms;


import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.concurrent.BlockingQueue;

import android.util.Log;


public class SMSRelayer extends Thread {
	
	
	private Socket socket;
	private PrintWriter out;
	private BlockingQueue<TextMessage> b;
	private SMSToolkitActivity activity;
	
	public SMSRelayer(SMSToolkitActivity a, Socket s) {
		socket = s;
		activity = a;
		
		try {
			out = new PrintWriter(socket.getOutputStream());
		} catch (IOException e) {
			Log.d("SMSRelayer", "Error opening output stream of socket");
		}
		
		b = TextMessageRelayQueue.getQueue();
	}
	
	
	
	@Override
	public void run() {
		
		
		
		Log.d("SMSRelayer", "Running...");
		boolean alive = true;
		while (alive) {
			
			TextMessage m = null;
			try {
				Log.d("SMSRelayer", "Waiting for sms...");
				m = b.take();
			} catch (InterruptedException e) {
				//pass!
			}
			
			if (m != null) {
				Log.d("SMSRelayer", "Received a testmessage!");
				activity.logReceive(m);
				out.write(m.toString());
				
				if (out.checkError() || socket.isClosed()) {
					Log.d("SMSRelayer", "unable to send it! shutting down");
					alive = false;
					b.add(m);
					
				}
			}
			
		}
		
	}
	
}