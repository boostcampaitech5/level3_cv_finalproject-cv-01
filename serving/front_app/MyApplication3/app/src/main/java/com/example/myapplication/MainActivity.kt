package com.example.myapplication

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import androidx.activity.result.contract.ActivityResultContracts
import com.example.myapplication.databinding.ActivityMainBinding
import com.google.gson.Gson
import org.json.JSONObject
import com.example.myapplication.JSONDATA
import java.io.File

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var info_frag: InfoFragment
    private val sharedData = SHARED_DATA
    private lateinit var bitmap: Bitmap
    val PERM_STORAGE = 9
    val PERM_CAMERA = 10
    val REQ_CAMERA = 11
    var IP: String? = null
    var PORT: Int? = null

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

        //data.json 파싱 및 데이터 저장
        dataParsing()

        //setting menu 설정
        val actionBar = supportActionBar
        setSupportActionBar(binding.mainToolbar)

        //카메라 버튼 및 설정
        binding.cameraImgView.setImageBitmap(sharedData.bitmap)
        val cameraLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()){

            result -> if (result.resultCode == RESULT_OK){
            val data = result.data
            Log.d("test",data!!.getStringExtra("from_activity").toString())
            when(data!!.getStringExtra("from_activity")){
                    "camera"->{
                        if (data!!.getBooleanExtra("success",false))
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

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_main,menu)
        return true
    }
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        Log.d("test", "onOptionsItemSelected - item ID: ${item.itemId}")
        return when (item.itemId) {
            R.id.checklist_settings -> {
                // Settings 메뉴 아이템을 클릭했을 때의 동작 처리
                val intent: Intent = Intent(this, SettingActivity::class.java)
                startActivity(intent)
                true
            }
            else -> super.onOptionsItemSelected(item)
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
    fun dataParsing(){
        //res.raw.data는 읽기 전용이기 떄문에 내부저장소에 파일 저장하는 형식으로 교체
        val file = File(filesDir,"user_data.json")
        val jsonString = file.readText()

        val gson = Gson()

        val data = gson.fromJson(jsonString, JSONDATA::class.java)
        sharedData.data = data.copy()

//        Log.d("test",data.class_dict.toString())
//        Log.d("test",data.ingredients_dict.toString())
//        Log.d("test",data.IP)
//        Log.d("test",data.PORT.toString())
//        Log.d("test",data.checklist.toString())
//        Log.d("test",data.checklist["egg"].toString())
    }

}

