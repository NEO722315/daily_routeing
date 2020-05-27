import java.util.LinkedList;

public class rand {
	
	public String decode(String s) {
		int multi = 0;
		StringBuilder result = new StringBuilder();
		LinkedList <Integer> stack_number = new LinkedList<>();
		LinkedList <String> stack_alpha = new LinkedList<>();
		for(char c : s.toCharArray()) {
			if(c=='[') {
				stack_number.addLast(multi);
				stack_alpha.addLast(result.toString());
				multi=0;
				result = new StringBuilder();
			}
			else if(c==']') {
				StringBuilder tmp = new StringBuilder();
				int cur_num = stack_number.removeLast();
				for(int i = 0;i<cur_num;i++) tmp.append(result.toString());
				result = new StringBuilder(stack_alpha.removeLast() + tmp.toString());
				System.out.println(result.toString());
			}
			else if(c>='0' && c<='9') multi = multi * 10 + Integer.parseInt(c+"");
			else result.append(c);
		}
		return result.toString();
	}
	
	public static void main(String args[]) {
		rand r = new rand();
		r.decode("3[a2[c]2[j]]");
	}
}



