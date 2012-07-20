package sobel.sms;

public class LogReceiveAction implements Runnable {

	
	private TextMessage message;
	private SMSToolkitActivity activity;
	
	public LogReceiveAction(TextMessage m, SMSToolkitActivity a) {
		message = m;
		activity = a;
	}
	
	
	public void run() {
		
		activity.logReceive(message);
		
	}
	
}
