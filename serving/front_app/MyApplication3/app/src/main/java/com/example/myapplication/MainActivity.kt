package com.example.myapplication

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import androidx.activity.result.contract.ActivityResultContracts
import com.example.myapplication.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var info_frag: InfoFragment
    private val sharedData = SHARED_DATA
    private lateinit var bitmap: Bitmap
    val PERM_STORAGE = 9
    val PERM_CAMERA = 10
    val REQ_CAMERA = 11


    private val REQUEST_IMAGE_CAPTURE = 2
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        info_frag = InfoFragment()
//        setContentView(R.layout.activity_main)
        setContentView(binding.root)

        //권한 획득
        requestPermissions(arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE),9)
        requestPermissions(arrayOf(Manifest.permission.CAMERA),PERM_CAMERA)
        //하단 정보 프래그먼트


        binding.cameraImgView.setImageBitmap(sharedData.bitmap)
        //카메라 버튼 및 설정
        val cameraLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()){

            result -> if (true){
                val data = result.data
                Log.d("test",data!!.getStringExtra("from_activity").toString())
                when(data!!.getStringExtra("from_activity")){
                    "camera"->{
                        binding.cameraImgView.setImageBitmap(sharedData.bitmap)
//                        Log.d("test","setImage:"+sharedData.image.toString())
                    }
                }
            }
        }
        binding.camera.setOnClickListener {
            val intent = Intent(this, CameraActivity::class.java)
            cameraLauncher.launch(intent)

        }
    }



    fun pushUpInfo(){

        val transaction = supportFragmentManager.beginTransaction()
        transaction.add(R.id.lower_frag, info_frag)
        transaction.addToBackStack("Info")
        transaction.commit()
    }
    fun pushDownInfo(){
        onBackPressed()
    }

}
fun test_camera(binding: ActivityMainBinding){
    binding.cameraImgView.setImageResource(R.drawable.sample_img)
}
fun camera_func(){
    Log.d("test","camera function")

}
//fun requirePermission(permissions: Array<String>, requestCode: Int){
//    Log.d("test","권한 요청")
//    if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) {
//        permissionGranted(requestCode)
//    } else {
//        // isAllPermissionsGranted : 권한이 모두 승인 되었는지 여부 저장
//        // all 메서드를 사용하면 배열 속에 들어 있는 모든 값을 체크할 수 있다.
//        val isAllPermissionsGranted =
//            permissions.all { checkSelfPermission(it) == PackageManager.PERMISSION_GRANTED }
//        if (isAllPermissionsGranted) {
//            permissionGranted(requestCode)
//        } else {
//            // 사용자에 권한 승인 요청
//            ActivityCompat.requestPermissions(this, permissions, requestCode)
//        }
//    }
//}