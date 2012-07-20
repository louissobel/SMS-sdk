package sobel.sms;

public class LogAction implements Runnable {

	
	private String message;
	private SMSToolkitActivity activity;
	
	public LogAction(String m, SMSToolkitActivity a) {
		message = m;
		activity = a;
	}
	
	
	public void run() {
		
		activity.log(message);
		
	}
	
}
