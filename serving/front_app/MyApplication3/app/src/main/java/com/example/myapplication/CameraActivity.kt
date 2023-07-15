package com.example.myapplication

import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.media.Image
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.Surface.ROTATION_0
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCaptureException
import androidx.camera.core.ImageProxy
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import com.example.myapplication.databinding.ActivityCameraBinding
import java.nio.ByteBuffer
import com.example.myapplication.SHARED_DATA
class CameraActivity : AppCompatActivity() {
    private lateinit var binding: ActivityCameraBinding
    private lateinit var imageCapture: ImageCapture
    private val sharedData = SHARED_DATA
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding =ActivityCameraBinding.inflate(layoutInflater)
        setContentView(binding.root)
        binding.revert.setOnClickListener {
            finish()
        }
        binding.capture.setOnClickListener{
            //카메라 권한은 있는데 비트맵을 못가져오는 문제 발생.
            val bitmap = captureCamera()
            sharedData.bitmap = bitmap


            val result = Intent().apply {
                putExtra("from_activity","camera")
                if(bitmap == null){
                    Log.d("test","Camera not available")
                    putExtra("success",false)
                }
                else{
                    putExtra("success",true)
                }
            }
            setResult(Activity.RESULT_OK,result)


            finish()
        }
        openCamera()
        imageCapture = ImageCapture.Builder().build()
    }
    fun captureCamera(): Bitmap?{
        var bitmap: Bitmap? = null
        imageCapture.takePicture(ContextCompat.getMainExecutor(this),
            object : ImageCapture.OnImageCapturedCallback(){
                override fun onCaptureSuccess(image: ImageProxy){
                    Log.d("test",image.imageInfo.toString())
                    bitmap = imageProxyToBitmap(image)
                }
                override fun onError(exception: ImageCaptureException) {
                    Log.d("test","image capture error:"+exception.message)

                }
        } )
        return bitmap
    }
    private fun imageProxyToBitmap(imageProxy: ImageProxy): Bitmap? {
        @androidx.camera.core.ExperimentalGetImage
        val image: Image? = imageProxy.image
        if (image != null) {
            val buffer: ByteBuffer = image.planes[0].buffer
            val pixelStride: Int = image.planes[0].pixelStride
            val rowStride: Int = image.planes[0].rowStride
            val rowPadding = rowStride - pixelStride * imageProxy.width

            // 비트맵 생성
            val bitmap = Bitmap.createBitmap(
                imageProxy.width + rowPadding / pixelStride,
                imageProxy.height,
                Bitmap.Config.ARGB_8888
            )

            // 이미지 데이터 추출
            bitmap.copyPixelsFromBuffer(buffer)

            image.close()
            return bitmap
        }
        return null
    }
    fun openCamera(){
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)

        cameraProviderFuture.addListener({
            // Used to bind the lifecycle of cameras to the lifecycle owner
            val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()

            // Preview
            val preview = Preview.Builder()
                .build()
                .also {
                    it.setSurfaceProvider(binding.viewFinder.surfaceProvider)
                }

            // Select back camera as a default
            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

            try {
                // Unbind use cases before rebinding
                cameraProvider.unbindAll()

                // Bind use cases to camera
                cameraProvider.bindToLifecycle(
                    this, cameraSelector, preview)

            } catch(exc: Exception) {
                Log.e("test", "Use case binding failed", exc)
            }

        }, ContextCompat.getMainExecutor(this))
    }
}