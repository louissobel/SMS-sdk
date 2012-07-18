package sobel.sms;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsMessage;
import android.util.Log;

public class SMSReceiver extends BroadcastReceiver {

	@Override
	public void onReceive(Context context, Intent intent) {

		Log.d("RECEIVER", "HERE got message!");
		Bundle bundle = intent.getExtras();
		SmsMessage message = null;

		String from = null;
		String to = null;
		String body = null;

		if (bundle != null) {
			// ---retrieve the SMS message received---
			Object[] pdus = (Object[]) bundle.get("pdus");

			if (pdus.length > 0) {

				message = SmsMessage.createFromPdu((byte[]) pdus[0]);
				from = message.getOriginatingAddress();
				to = ""; // me?

				body = message.getMessageBody().toString();
				
				TextMessageRelayQueue.getQueue().add(new TextMessage(to,from,body));
				
				Log.d("RECEIVER", "added message to queue message!");
			}
		}
	}
}
