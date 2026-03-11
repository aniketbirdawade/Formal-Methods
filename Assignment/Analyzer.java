import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Analyzer 
{
    public static void main(String[] args) throws Exception
    {
        
        File file = new File("DemoProgram.java");
        BufferedReader br = new BufferedReader(new FileReader(file));

        Map<String, Integer> operator = new HashMap<>();
        Map<String, Integer> symbol = new HashMap<>();
        Map<String, Integer> keyword = new HashMap<>();
        Map<String, Integer> function = new HashMap<>();
        Map<String, Integer> variables = new HashMap<>();

        String line;

        while ((line = br.readLine()) != null) 
        {
            count(line, "\\+", operator, "+"); 
            count(line, "-", operator, "-");
            count(line, "\\*", operator, "*");
            count(line, "/", operator, "/");

            count(line, "\\{", symbol, "{");
            count(line, "\\}", symbol, "}");
            count(line, "\\(", symbol, "(");
            count(line, "\\)", symbol, ")");

            count(line, "class", keyword, "class");
            count(line, "public", keyword, "public");
            count(line, "private", keyword, "private");
            count(line, "static", keyword, "static");

    // Detect functions

            Pattern pattern = Pattern.compile("(\\w+)\\s*\\(");
            Matcher matcher = pattern.matcher(line);

            while(matcher.find())
            {
                String name = matcher.group(1);
                
                if(!name.equals("if") && !name.equals("for") && !name.equals("while"))
                {
                    function.put(name, function.getOrDefault(name, 0)+1);
                }
            }

    // Detect Variables
            Pattern varpattern = pattern.compile("(int | String | double | float | boolean)\\s+(\\w+)");
            Matcher varmatcher = varpattern.matcher(line);

            while (varmatcher.find()) {
                String var = varmatcher.group(2);
                variables.put(var, variables.getOrDefault(var, 0) + 1);
                
            }
        }
        br.close();

        System.out.println("-----Final Analyzer Output-----\n\n");

        printMap("Function Name: \tCount", function);
        printMap("Variables: Count", variables);
        printMap("Operators: Count", operator);
        printMap("Symbols: Count", symbol);
        printMap("Keywords: Count", keyword);
    }
    
    static void count(String line, String regex, Map<String, Integer> map, String key)
    {
        Matcher m = Pattern.compile(regex).matcher(line);
        while (m.find()) 
            {
                map.put(key, map.getOrDefault(key, 0) + 1);
        }
    }

    static void countWord(String line, String word, Map<String, Integer> map)
    {
        Pattern p = Pattern.compile("\\b" + word + "\\b");
        Matcher m = p.matcher(line);
        while (m.find()) 
            {
                map.put(word, map.getOrDefault(word, 0) + 1);
        }
    }

    static void printMap(String title, Map<String, Integer> map)
    {
        System.out.println(title + ":");
        for (String key : map.keySet()) 
            {
                System.out.println(key + " -> " + map.get(key));
        }
        System.out.println();
    }
}
