package sobel.sms;

import java.util.concurrent.LinkedBlockingQueue;

public class TextMessageRelayQueue {

	
	
	private static TextMessageRelayQueue theInstance = null;
	
	
	private LinkedBlockingQueue<TextMessage> queue;
	
	
	public static synchronized LinkedBlockingQueue<TextMessage> getQueue() {
		
		if (theInstance == null) {
			theInstance = new TextMessageRelayQueue();
		}
		
		return theInstance.queue;
		
		
	}
	
	
	private TextMessageRelayQueue() {
		queue = new LinkedBlockingQueue<TextMessage>();
	}
	
	
	
	
}
