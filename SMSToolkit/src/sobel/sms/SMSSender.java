package sobel.sms;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

import android.app.PendingIntent;
import android.content.Intent;
import android.telephony.SmsManager;
import android.util.Log;


public class SMSSender extends Thread {

	private Socket socket;
	
	private SmsManager smsManager = SmsManager.getDefault();
	private SMSToolkitActivity activity;
	
	public SMSSender(SMSToolkitActivity a, Socket s) {
		activity = a;
		socket = s;
	}

	@Override
	public void run() {

		try {
			BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

			TextMessageParser parser = new TextMessageParser(in);
			
			System.err.println("HERE");
			
			for (TextMessage message = parser.getOne(); message != null; message = parser.getOne()) {

				//I have to send the message!
				Log.d("SMSSender",String.format("Trying to send: %s",message.getBody()));

				try {
					smsManager.sendTextMessage(message.to, null, message.getBody(), null, null);
					activity.logSend(message);
				} catch (Exception e) {
					//TODO
					//Error sending the SMS!!!
					Log.d("SMSSender", "Error sending the sms!");
				}
			}
			
			//here, I should close the connection ASAP
			socket.close();
			

		} catch (IOException e) {
			// TODO
		}

	}

}
