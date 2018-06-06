package ReverseHash;

import java.util.Scanner;

public class Solution {

	public static void main(String[] args) {
		
		Scanner userInputScanner = new Scanner(System.in);
		long hashValInput = userInputScanner.nextLong();
		ReverseHashHelper reverseHash = new ReverseHashHelper();
		System.out.println(reverseHash.getString(hashValInput));
	}

}
