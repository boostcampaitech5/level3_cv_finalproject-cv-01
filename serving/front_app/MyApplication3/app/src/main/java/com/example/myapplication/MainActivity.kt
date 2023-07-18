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
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.File
import com.example.myapplication.serverData
import com.example.myapplication.clientData
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var info_frag: InfoFragment
    private val sharedData = SHARED_DATA
    private lateinit var bitmap: Bitmap
    val PERM_STORAGE = 9
    val PERM_CAMERA = 10
    val REQ_CAMERA = 11
    lateinit var url_string:String
    private lateinit var retrofit:Retrofit
    private lateinit var service: RetrofitService
    private val REQUEST_IMAGE_CAPTURE = 2
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        info_frag = InfoFragment()
        setContentView(binding.root)

        //권한 획득
//        requestPermissions(arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE),9)
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
                        //send버튼 활성화
                            binding.connectServer.isEnabled = true
                    }
                }
            }
        }
        binding.camera.setOnClickListener {
            val intent = Intent(this, CameraActivity::class.java)
            cameraLauncher.launch(intent)

        }
        //http 통신 설정
        Log.d("test",url_string)
        retrofit = Retrofit.Builder().baseUrl(url_string)
            .addConverterFactory(GsonConverterFactory.create()).build()
        service = retrofit.create(RetrofitService::class.java)
        // 서버 접속 버튼
        binding.connectServer.setOnClickListener{
            Log.d("test","serverconnect_listener")
            binding.connectServer.isEnabled = false
            connectServer()
        }
//        connectServer()
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
    fun connectServer(){
        //서버 통신 테스트용
//        service.test().enqueue(object :Callback<String>{
//            override fun onResponse(call: Call<String>, response: Response<String>) {
//                Log.d("test",response.toString())
//            }
//
//            override fun onFailure(call: Call<String>, t: Throwable) {
//                Log.d("test","test fail")
//            }
//        })

        val data:clientData = clientData(sharedData.image_byte!!)

        service.getResult(data).enqueue(object : Callback<serverData> {
            override fun onResponse(call: Call<serverData>, response: Response<serverData>) {
                Log.d("test","return : ${response.toString()}")
                Log.d("test",response.body()!!.toString())
            }
            override fun onFailure(call: Call<serverData>, t: Throwable) {
                Log.d("test","fail: ${t.printStackTrace()}")
            }
        })


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
        var jsonString:String
        var data:JSONDATA
        val gson = Gson()
        if (!file.exists()){
            val resourceId = resources.getIdentifier("data","raw",packageName)
            val inputStream = resources.openRawResource(resourceId)
            jsonString = inputStream.bufferedReader().use{it.readText()}
            data = gson.fromJson(jsonString, JSONDATA::class.java)
        }
        else {
            jsonString = file.readText()
            data = gson.fromJson(jsonString, JSONDATA::class.java)

            //data version이 달라질 경우 초기화하는 코드
            val resourceId = resources.getIdentifier("data","raw",packageName)
            val inputStream = resources.openRawResource(resourceId)
            val origin_jsonString = inputStream.bufferedReader().use{it.readText()}
            val original_data = gson.fromJson(origin_jsonString, JSONDATA::class.java)
            if (data.version != original_data.version){
                data = original_data
            }
        }


       // var data = gson.fromJson(jsonString, JSONDATA::class.java)

        sharedData.data = data.copy()
        url_string = "http://"+data.IP +":"+ data.PORT.toString()
//        Log.d("test",data.class_dict.toString())
//        Log.d("test",data.ingredients_dict.toString())
//        Log.d("test",data.IP)
//        Log.d("test",data.PORT.toString())
        Log.d("test",data.checklist.toString())
//        Log.d("test",data.checklist["egg"].toString())
    }

}

