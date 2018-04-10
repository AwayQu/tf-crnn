//
//  TextDetection.swift
//  vision_text_detection
//
//  Created by MacDev on 2018/4/9.
//  Copyright © 2018年 MacDevHuang. All rights reserved.
//

import Cocoa
import Vision
import CoreML


class TextDetection: NSObject {
    var boxes: [VNRectangleObservation] = []
    
    //HOLDS OUR INPUT
    var  inputImage:CIImage?
    
    //RESULT FROM OVERALL RECOGNITION
    var  recognizedWords:[String] = [String]()
    
    //RESULT FROM RECOGNITION
    var recognizedRegion:String = String()
    

    var resultImgs:[CIImage] = [CIImage]()
    
    //TEXT-DETECTION-REQUEST
    lazy var textDetectionRequest: VNDetectTextRectanglesRequest = {
        return VNDetectTextRectanglesRequest(completionHandler: self.handleDetection)
    }()
    
    var semaphore:DispatchSemaphore! = nil
    
    //TEXT-DETECTION-HANDLER
    func handleDetection(request:VNRequest, error: Error?)
    {
        guard let observations = request.results as? [VNTextObservation]
            else {fatalError("unexpected result") }
        
        // EMPTY THE RESULTS
        self.recognizedWords = [String]()
        
        //NEEDED BECAUSE OF DIFFERENT SCALES
        let  transform = CGAffineTransform.identity.scaledBy(x: (self.inputImage?.extent.size.width)!, y:  (self.inputImage?.extent.size.height)!)
        
        //A REGION IS LIKE A "WORD"
        for region:VNTextObservation in observations
        {
            guard let boxesIn = region.characterBoxes else {
                continue
            }
            
            //EMPTY THE RESULT FOR REGION
            self.recognizedRegion = ""
            
            //A "BOX" IS THE POSITION IN THE ORIGINAL IMAGE (SCALED FROM 0... 1.0)
            for box in boxesIn
            {
                
                self.boxes.append(box)
                
                //SCALE THE BOUNDING BOX TO PIXELS
                let realBoundingBox = box.boundingBox.applying(transform)
                
                //TO BE SURE
                guard (inputImage?.extent.contains(realBoundingBox))!
                    else { print("invalid detected rectangle"); return}
                
                //SCALE THE POINTS TO PIXELS
                let topleft = box.topLeft.applying(transform)
                let topright = box.topRight.applying(transform)
                let bottomleft = box.bottomLeft.applying(transform)
                let bottomright = box.bottomRight.applying(transform)
                
                //LET'S CROP AND RECTIFY
                let charImage = inputImage?
                    .cropped(to: realBoundingBox)
                    .applyingFilter("CIPerspectiveCorrection", parameters: [
                        "inputTopLeft" : CIVector(cgPoint: topleft),
                        "inputTopRight" : CIVector(cgPoint: topright),
                        "inputBottomLeft" : CIVector(cgPoint: bottomleft),
                        "inputBottomRight" : CIVector(cgPoint: bottomright)
                        ])
                
                self.resultImgs.append(charImage!)
            }
            

        }
        
        
        self.semaphore.signal()
        
    }

    
    func textDetect(ciImage:CIImage)
    {
        self.semaphore.wait()
        //PREPARE THE HANDLER
        let handler = VNImageRequestHandler(ciImage: ciImage, options:[:])
        
        //WE NEED A BOX FOR EACH DETECTED CHARACTER
        self.textDetectionRequest.reportCharacterBoxes = true
        self.textDetectionRequest.preferBackgroundProcessing = false
        
        //FEED IT TO THE QUEUE FOR TEXT-DETECTION
        DispatchQueue.global(qos: .userInteractive).async {
            do {
                try  handler.perform([self.textDetectionRequest])
            } catch {
                print ("Error")
            }
        }
        
    }
    
}




