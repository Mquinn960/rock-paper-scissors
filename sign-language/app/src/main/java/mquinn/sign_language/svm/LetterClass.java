package mquinn.sign_language.svm;

public enum LetterClass {

    NONE(0),
    ROCK(1),
    PAPER(2),
    SCISSORS(3),
    ERROR(99);

    private int letterIndex;

    private LetterClass(int letterIndex) {
        this.letterIndex = letterIndex;
    }

    public static LetterClass getLetter(int legIndex) {
        for (LetterClass l : LetterClass.values()) {
            if (l.letterIndex == legIndex) return l;
        }
        return LetterClass.ERROR;
    }

    public static int getIndex(String letter) {
        for (LetterClass l : LetterClass.values()) {
            if (l.toString().equals(letter)) return l.letterIndex;
        }
        throw new IllegalArgumentException("Index not found");
    }

    // Example usage

    //  int myLetterIndex = 1;
    //  expected : A
    //  LetterClass myLetter = LetterClass.getLetter(myLetterIndex);

}
