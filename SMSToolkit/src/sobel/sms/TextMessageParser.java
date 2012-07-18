package sobel.sms;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 
 * Message Parser is a state machine class that parses a subset of text
 * representing a message into the components of the data-type, Message. Takes a
 * buffered reader and reads it by line it reads through a full message.
 */
public class TextMessageParser {


	// for separating out key,value
	public static final Pattern headerParser = Pattern.compile("(LENGTH|TO|FROM):(.*)");


	private BufferedReader in;

	/**
	 * 
	 * @param in
	 *            BufferedReader to parse
	 */
	public TextMessageParser(BufferedReader in) {
		this.in = in;

	}

	/**
	 * Reads lines from the BufferedReader and returns messages. If an invalid
	 * message is sent, a RuntimeException thrown
	 * 
	 * @return Message
	 */
	public TextMessage getOne() {

		String state = "waiting";

		int length = 0;

		int bodyLinesRemaining = 0;
		StringBuilder bodyBuilder = new StringBuilder();

		String to = null;
		String from = null;
		String body = null;

		while (true) {
	
			String input;
			try {
				input = in.readLine();
			} catch (IOException e) {
				// in socket closed, so return null
				return null;
			}

			if (input == null) {
				return null;
			}

			// TYPE MODE
			if (state.equals("waiting")) {


				if (input.equals("TEXT")) {
					state = "headers";
				} else {
					// then this was an invalid input for type mode
					throw new RuntimeException(String.format(
							"Invalid line while waiting for text: %s", input));
				}

				// HEADER MODE
			} else if (state.equals("headers")) {

				Matcher headerMatch = headerParser.matcher(input);

				if (headerMatch.matches()) {


					String key = headerMatch.group(1);
					String value = headerMatch.group(2);

					if (key.equals("LENGTH")) {
						// due to the regex, we know that the value is a
						// int-parseable value
						length = Integer.parseInt(value);
					} else if (key.equals("TO")) {
						// out cannot be null if the states are working. maybe
						// check?
						to = value;
					} else {
						//it must be from
						from = value;
					}

				} else if (input.equals("")) {
					// then we are done with headers
					if (length == 0) {
						body = "";
						return new TextMessage(to, from, body);
					} else {
						state = "body";
						bodyLinesRemaining = length;
					}
				} else {
					// then this was in invalid line for header mode
					throw new RuntimeException(String.format(
							"Invalid line while parsing headers: %s", input));
				}
			} else if (state.equals("body")) {
				bodyBuilder.append(input + "\n");
				bodyLinesRemaining--;

				if (bodyLinesRemaining == 0) {
					// then we have slurped up all the body that we need to
					body = bodyBuilder.toString();
					return new TextMessage(to, from, body);
				}

			} else {
				throw new RuntimeException(String.format(
						"Invalid state in message parser: %s", state));
			}
			

		}

	}

}
