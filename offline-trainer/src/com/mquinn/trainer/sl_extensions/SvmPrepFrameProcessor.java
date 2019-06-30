package com.mquinn.trainer.sl_extensions;

import mquinn.sign_language.imaging.IFrame;
import mquinn.sign_language.processing.IFrameProcessor;
import mquinn.sign_language.svm.LetterClass;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Size;

import java.io.File;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SvmPrepFrameProcessor implements IFrameProcessor {

    private IFrame workingFrame;
    private File workingFile;
    private SvmInputData trainingData;
    private Mat flatFeatures, singleLabel;
    private int letterLabel;

    public SvmPrepFrameProcessor(){

        trainingData = new SvmInputData();

        flatFeatures = new Mat();
        flatFeatures.convertTo(flatFeatures, CvType.CV_32FC1);

        trainingData.samples.convertTo(trainingData.samples,  CvType.CV_32FC1);

    }

    public IFrame process(IFrame inputFrame) {

        workingFrame = inputFrame;

        compileData();

        return workingFrame;

    }

    private void compileData(){
        flattenFeatures();

        flatFeatures.convertTo(flatFeatures, CvType.CV_32FC1);

        String[] data = workingFile.getName().split("_");
        String letter = data[0];

        resolveLetterLabel(letter);

        singleLabel = new Mat( new Size( 1, 1 ), CvType.CV_32SC1 );
        singleLabel.put(0,0, (int)letterLabel);

        trainingData.labels.push_back(singleLabel);
        trainingData.samples.push_back(flatFeatures);

        flatFeatures.release();
        singleLabel.release();

        Logger.getAnonymousLogger().log(Level.INFO, "CLASS: " + LetterClass.getLetter(letterLabel));

    }

    public void setInputFile(File inputFile){
        workingFile = inputFile;
    }

    public SvmInputData getTrainingData(){
        return trainingData;
    }

    private void resolveLetterLabel(String inputLetter){
        if (inputLetter.matches("[A-Z]+")) {
            letterLabel = LetterClass.getIndex(inputLetter);
        } else {
            letterLabel = LetterClass.getIndex("ERROR");
        }
    }

    private void flattenFeatures(){
        flatFeatures = workingFrame.getHogDesc();
        flatFeatures = flatFeatures.reshape(1,1);
    }

}
