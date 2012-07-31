package sobel.sms;





/**
 * 
 * The class represents a message, which contains information about the type of
 * message, the set of headers, and the body (if it is a message).
 * 
 */
public class TextMessage {

	public String to;
	public String from;
	public String body;

	/**
	 * 
	 * @param type
	 *            String representing the type of the message being initiated
	 */

	public TextMessage(String t, String f, String b) {
		to = t;
		from = f;
		body = b;
		
		if (t == null) {
			throw new RuntimeException("To cannot be null");
		}
		
		if (f == null) {
			throw new RuntimeException("From cannot be null");
		}
		
		if (b == null) {
			throw new RuntimeException("Body cannot be null");
		}
	}

	public void trim() {
		body = body.substring(0, body.length() - 1);
	}
	
	public String getBody() {
		//returns the body but with a trailing newline, if any, removed;
		//no, thats not true - we have to add a '\n' if its empty!
		//no we don't!		
		return body;
	}


	@Override
	public String toString() {

		StringBuilder b = new StringBuilder();

		int length = 0;
		
		String outBody = body + '\n';
		int len = outBody.length();
		
		for (int pos = 0; pos < len; pos++) {
			char c = outBody.charAt(pos);
			if (c == '\n') {
				length++;
			}
		}		


		b.append("TEXT\n");

		b.append("LENGTH:" + length + '\n');
		
		b.append(String.format("TO:%s\n",to));
		b.append(String.format("FROM:%s\n",from));

		b.append("\n"); // end headers

		b.append(outBody);

		return b.toString();
	}

}
