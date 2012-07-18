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

	
	public String getBody() {
		//returns the body but with a trailing newline, if any, removed;
		//no, thats not true - we have to add a '\n' if its empty!
		int len = body.length();
		
		if (len == 0) {
			return "\n";
		} else {
			if (body.charAt(len - 1) == '\n') {
				return body.substring(0, len - 1);
			} else {
				return body;
			}
		}
	}


	@Override
	public String toString() {

		StringBuilder b = new StringBuilder();

		int length = 0;

		int len = body.length();
			
		if (len == 0) {
			body = "\n";
		} else {
			if (body.charAt(len - 1) != '\n') {
				body = body + '\n';
				len++;
			}
			for (int pos = 0; pos < len; pos++) {
				char c = body.charAt(pos);
				if (c == '\r') {
					length++;
					if (pos + 1 < len && body.charAt(pos + 1) == '\n') {
						pos++;
					}
				} else if (c == '\n') {
					length++;
				}
			}
		}



		b.append("TEXT\n");

		b.append("LENGTH:" + length + '\n');
		
		b.append(String.format("TO:%s\n",to));
		b.append(String.format("FROM:%s\n",from));

		b.append("\n"); // end headers

		b.append(body);

		return b.toString();
	}

}
