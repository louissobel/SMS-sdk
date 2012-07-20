package sobel.sms;

public class LogSendAction implements Runnable {

	
	private TextMessage message;
	private SMSToolkitActivity activity;
	
	public LogSendAction(TextMessage m, SMSToolkitActivity a) {
		message = m;
		activity = a;
	}
	
	
	public void run() {
		
		activity.logSend(message);
		
	}
	
}
