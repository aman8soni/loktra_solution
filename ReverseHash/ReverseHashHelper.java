package ReverseHash;

public class ReverseHashHelper {

	private String letters = "acdegilmnoprstuw";
	private final int HASH_CONST = 37;
	private final int MIN_VAL = 7;

	public String getString(long hash) {
		String resultString = "";
		long l_hash = hash;
		while (l_hash > MIN_VAL) {
			resultString = letters.charAt((int) (l_hash % HASH_CONST)) + resultString;
			l_hash = l_hash / HASH_CONST;
		}
		return resultString;
	}

}
