/*
* Licensed to the Apache Software Foundation (ASF) under one
* or more contributor license agreements.  See the NOTICE file
* distributed with this work for additional information
* regarding copyright ownership.  The ASF licenses this file
* to you under the Apache License, Version 2.0 (the
* "License"); you may not use this file except in compliance
* with the License.  You may obtain a copy of the License at
*
*   http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing,
* software distributed under the License is distributed on an
* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied.  See the License for the
* specific language governing permissions and limitations
* under the License.
*/

package corpus.sinhala;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.LinkedList;
import org.apache.log4j.Logger;

/**
 * Use splitWords() and splitSentences() to split texts
 * @author lahiru
 */
public class SinhalaTokenizer {
    
    private final LinkedList<String> ignoringCharList;
    
    private boolean isolatePunctuationsWithSpaces;
    
    private final String punctuationMarks[] = {".", ",", "\n", " ", "¸", "‚",
                                    "\"", "/", "-", "|", "\\", "—", "¦",
                                    "”", "‘", "'", "“", "’", "´", "´",
                                    "!", "@", "#", "$", "%", "^", "&", "\\*", "+", "\\-", "£", "\\?", "˜",
                                    "\\(", "\\)", "\\[", "\\]", "{", "}",
                                    ":", ";",
                                    "\u2013" /*EN-DASH*/
                                    };
    
    // these are invalid but separating 2 words. So, should be replaced by a space
    private final String invalidChars[] = {"Ê",
                                    "\u00a0", "\u2003", // spaces
                                    "\ufffd", "\uf020", "\uf073", "\uf06c", "\uf190", // unknown or invalid unicode chars
                                    "\u202a", "\u202c", "\u200f" //  direction control chars (for arabic, starting from right etc)
                                    };
    
    private final String numbers[] = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"};
    
    private final String wordTokenizerDelims;
    
    private final String lineTokenizingChars[] = {".", "?", "!", ":", ";", "\u2022"};
    
    private final String punctuationsWithoutLineTokenizingChars[] = {",", "¸", "‚",
                                                                    "\"", "/", "-", "\\|", "\\\\", "—", "¦",
                                                                    "”", "‘", "'", "“", "’", "´", "´",
                                                                    "!", "@", "#", "\\$", "\\%", "\\^", "\\&", 
                                                                    "\\*", "\\+", "\\-", "£", "\\?", "˜",
                                                                    "\\(", "\\)", "\\[", "\\]", "\\{", "\\}",
                                                                    ":", ";",
                                                                    "\u2013"
                                                                    };
    
    private final String shortForms[] = {"ඒ\\.", "බී\\.", "සී\\.", "ඩී\\.", "ඊ\\.", "එෆ්\\.", "ජී\\.", "එච්\\.",
                                        "අයි\\.", "ජේ\\.", "කේ\\.", "එල්\\.", "එම්\\.", "එන්\\.", "ඕ\\.",
                                        "පී\\.", "කිව්\\.", "ආර්\\.", "එස්\\.", "ටී\\.", "යූ\\.", "ඩබ්\\.", "ඩබ්ලිව්\\.",
                                        "එක්ස්\\.", "වයි\\.", "ඉසෙඩ්\\.",
                                        "පෙ\\.", "ව\\.", "ප\\.",
                                        "රු\\.",
                                        "0\\.", "1\\.", "2\\.", "3\\.", "4\\.", "5\\.", "6\\.", "7\\.", "8\\.", "9\\."
                                       };
    
    private final String shortFormIdentifier = "\u0D80"; // this is an unassigned letter of sinhala block
    
    private final String lineTokenizerDelims;
    
    private final static Logger logger = Logger.getLogger(Util.class);
    
    private void initIgnoringChars() {
        ignoringCharList.addLast("\u200c");
        ignoringCharList.addLast("\u0160");
        ignoringCharList.addLast("\u00ad");
        ignoringCharList.addLast("\u0088");
        ignoringCharList.addLast("\uf086");
        ignoringCharList.addLast("\u200b");
        ignoringCharList.addLast("\ufeff");
                
        // read ignoring characters from resources/ignoringCharList.txt
        InputStream is = SinhalaTokenizer.class.getClassLoader().getResourceAsStream("ignoringCharList.txt");
        BufferedReader br = new BufferedReader(new InputStreamReader(is));
        String word;
        try {
            while((word = br.readLine()) != null) {
                ignoringCharList.addLast(word.trim());
            }
        } catch (IOException ex) {
            logger.error(ex);
        }
    }
    
    public SinhalaTokenizer() {
        isolatePunctuationsWithSpaces = false;
        
        for(String s : punctuationsWithoutLineTokenizingChars) {
            if(s.equals(shortFormIdentifier)) {
                System.out.println("Do not use " + shortFormIdentifier + " at punctuation list.");
                System.exit(-1);
            }
        }
        
        // init ignoring chars
        ignoringCharList = new LinkedList<String>();
        initIgnoringChars();
        
        // init word tokenizer
        String tmp = "[";
        for(String s : punctuationMarks) {
            tmp += s;
        }
        for(String s : invalidChars) {
            tmp += s;
        }
        for(String s : numbers) {
            tmp += s;
        }
        tmp += "]";
        wordTokenizerDelims = tmp;
        
        // init line tokenizer
        tmp = "[";
        for(String s : lineTokenizingChars) {
            tmp += s;
        }
        tmp += "]";
        lineTokenizerDelims = tmp;
    }
    
    private boolean isASinhalaLetter(String s) {
       if(s.length() != 1) return true;
       int sinhalaLowerBound = 3456;
       int sinhalaUpperBound = 3583;

       int cp = s.codePointAt(0);
       if(cp >= sinhalaLowerBound && cp <= sinhalaUpperBound) {
           return true;
       }
       return false;
    }
    
    private boolean containsSinhala(String s) {
        for(int i = 0; i < s.length(); ++i) {
            if(isASinhalaLetter(s.charAt(i) + "")) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * split the Sinhala text to words
     * @param str String to be splited
     * @return LinkedList of the sentences
     */
    public LinkedList<String> splitWords(String str) {
        // remove ignoring chars from document
        for(String ignoringChar : ignoringCharList) {
            if(str.contains(ignoringChar)) {
                str = str.replaceAll(ignoringChar, "");
            }
        }
        
        String parts[] = str.split(wordTokenizerDelims);
        LinkedList<String> list = new LinkedList<String>();
        for(String word : parts) {
            // filter symbols
            if(word.length() == 1 && !isASinhalaLetter(word)) {
                continue;
            }
            
            // if no sinhala chars are present
            if(Util.getSinhalaOnlyRatio(word) == 0) {
                continue;
            }
            
            // add accpted words to list
            if(!word.equals("")) {
                list.addLast(word);
            }
        }
        return list;
    }
    
    /**
     * split the Sinhala text to sentences
     * @param str String to be splited
     * @return LinkedList of the sentences
     */
    public LinkedList<String> splitSentences(String str) {
        LinkedList<String> sentenceList = new LinkedList<String>();
        // remove ignoring chars from document
        for(String ignoringChar : ignoringCharList) {
            if(str.contains(ignoringChar)) {
                str = str.replaceAll(ignoringChar, "");
            }
        }
        
        // prevent short froms being splitted into sentences
        // Eg: පෙ.ව.
        for(String shortForm : shortForms) {
            String representation = shortForm.substring(0, shortForm.length() - 1) + shortFormIdentifier;
            str = str.replaceAll(shortForm, representation);
        }
        
        //split lines
        String parts[] = str.split(lineTokenizerDelims);
        for(String sentence : parts) {
            sentence = sentence.replaceAll(shortFormIdentifier, ".");
            sentence = sentence.trim();
            
            if(containsSinhala(sentence)) {    // filter empty sentences and non-sinhala sentences
                sentenceList.addLast(sentence);
            }
        }
        return sentenceList;
    }
    
    // example implementation
    public static void main(String[] args) {
        SinhalaTokenizer st = new SinhalaTokenizer();
//        String text = "මෙම උපාධිධාරියා පිළිබඳව තොරතුරු දැනගත් වහාම අධ්‍යාපන" +
//                      " අමාත්‍යාංශ ලේකම් එච්. එම්. ගුණසේකර මහතා ඔහු අමාත්‍යාංශයට කැඳවා පරීක්‌ෂා කර තිබේ";
        
        String text = "කොළඹ ප්‍රධාන පෙළේ ජාතික පාසලකට දෙමළ මාධ්‍ය කර්ණාට ගුරුවරියක" +
                        " අනුයුක්‌ත කර ඇති අතර එම පාසලේ දෙමළ මාධ්‍යයෙන් කර්ණාට සංගීත විෂයය ඉගෙන ගන්නා සිසුන්" +
                        " නැත. මේ නිසා විදුහල්පතිවරයා ගුරුවරියට ප්‍රකාශ කර ඇත්තේ වෙනත් විෂයයක්‌ උගන්වන ලෙසය." +
                        " ඇතැම් කලාපවලට යෑවූ ගුරුවරුන්ට පුරප්පාඩු නොමැති වීම නිසා පත්වීම් ලබාදී නැති අතර මෙම" +
                        " තත්ත්වය යටතේ එම උපාධිධාරීහු දැඩි අපහසුතාවට පත්වූහ.";
        LinkedList<String> words = st.splitWords(text);
        System.out.println("words:");
        for(String s : words) {
            System.out.println(s);
        }
        LinkedList<String> sentences = st.splitSentences(text);
        System.out.println("sentences:");
        for(String s : sentences) {
            System.out.println(s);
        }
    }
    
}
