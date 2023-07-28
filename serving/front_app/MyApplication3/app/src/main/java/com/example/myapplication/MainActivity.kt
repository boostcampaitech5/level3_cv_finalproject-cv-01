package com.example.myapplication

import android.Manifest
import android.app.Activity
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ImageDecoder
import android.net.Uri
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.annotation.RequiresApi
import androidx.core.content.FileProvider
import androidx.core.net.toUri

import com.example.myapplication.databinding.ActivityMainBinding
import com.google.gson.Gson
import com.theartofdev.edmodo.cropper.CropImage
import com.theartofdev.edmodo.cropper.CropImageActivity
import com.theartofdev.edmodo.cropper.CropImageView
import com.theartofdev.edmodo.cropper.CropImageView.CropResult
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.File
import okhttp3.OkHttpClient
import java.io.ByteArrayOutputStream
import java.io.FileOutputStream
import java.io.OutputStream
import java.nio.ByteBuffer
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var info_frag: ResultListDialog
    private lateinit var bitmap: Bitmap
    val PERM_STORAGE = 9
    val PERM_CAMERA = 10
    val REQ_CAMERA = 11
    lateinit var url_string:String
    private lateinit var retrofit:Retrofit
    private lateinit var service: RetrofitService
    private val REQUEST_IMAGE_CAPTURE = 2
    private lateinit var uri:Uri
    @RequiresApi(Build.VERSION_CODES.P)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)

        setContentView(binding.root)

        //권한 획득
//        requestPermissions(arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE),9)
        requestPermissions(arrayOf(Manifest.permission.CAMERA),PERM_CAMERA)




        //data.json 파싱 및 데이터 저장
        dataParsing()


        //하단 정보 프래그먼트
        info_frag = ResultListDialog()
        supportFragmentManager.beginTransaction()
            .add(R.id.info_container,info_frag)
            .commit()
        //setting menu 설정
        val actionBar = supportActionBar
        setSupportActionBar(binding.mainToolbar)


        val cropLauncher =registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == RESULT_OK) {
                val crop_result = CropImage.getActivityResult(result.data)

                SHARED_DATA.bitmap = ImageDecoder.decodeBitmap(ImageDecoder
                    .createSource(application.contentResolver,crop_result.uri))
                SHARED_DATA.bitmap = Bitmap.createScaledBitmap(SHARED_DATA.bitmap!!,224,224,true)
                Log.d("test","${SHARED_DATA!!.bitmap!!.height}")
                val out_stream = ByteArrayOutputStream()
                SHARED_DATA.bitmap!!.compress(Bitmap.CompressFormat.JPEG,100,out_stream)
                SHARED_DATA.image_byte = out_stream.toByteArray()
                binding.cameraImgView.setImageBitmap(SHARED_DATA.bitmap)
                binding.connectServer.isEnabled = true
            }
        }
        val cameraLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == RESULT_OK) {
                val capture_data: Intent? = result.data
//                val imageBitmap = capture_data?.extras?.get("data") as Bitmap

//                Log.d("test","${imageBitmap.height}")
                Log.d("test","${uri}")
//                val uri = saveBitmapToCacheUri(this,imageBitmap)
//                binding.cameraImgView.setImageURI(uri)
//                Log.d("test","Uri:${uri}")
                val crop_activity = CropImage.activity(uri)
                    .setGuidelines(CropImageView.Guidelines.ON)
                    .setAspectRatio(1,1)

                val crop_intent = crop_activity.getIntent(this)
                cropLauncher.launch(crop_intent)
            }
        }

        val galleryLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == RESULT_OK) {
                val capture_data: Intent? = result.data
                val gallery_uri = capture_data?.data
                val crop_activity = CropImage.activity(gallery_uri)
                    .setGuidelines(CropImageView.Guidelines.ON)
                    .setAspectRatio(1,1)
                val crop_intent = crop_activity.getIntent(this)
                cropLauncher.launch(crop_intent)
            }
        }

        //카메라 버튼 및 설정
        binding.cameraImgView.setImageBitmap(SHARED_DATA.bitmap)

        uri = FileProvider.getUriForFile(this,
            "${applicationContext.packageName}.fileprovider",
            File(this.cacheDir,"temp.jpg"))
        binding.camera.setOnClickListener {

                val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)

                intent.putExtra(MediaStore.EXTRA_OUTPUT,uri)
                cameraLauncher.launch(intent)

        }

        //갤러리 설정
        binding.galleryBtn.setOnClickListener{
            val intent = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
            galleryLauncher.launch(intent)
        }


        //http 통신 설정
        Log.d("test",url_string)
        retrofit = Retrofit.Builder()
            .client(OkHttpClient.Builder()
                .callTimeout(330,TimeUnit.SECONDS)
                .connectTimeout(330,TimeUnit.SECONDS)
                .build())
            .baseUrl(url_string)
            .addConverterFactory(GsonConverterFactory.create()).build()
        service = retrofit.create(RetrofitService::class.java)
        // 서버 접속 버튼
        binding.connectServer.setOnClickListener{

            Log.d("test","${SHARED_DATA.bitmap!!.height},${SHARED_DATA.bitmap!!.width}")
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
    fun setBottomSheet(server_data: serverData){
        info_frag.setInfoData(server_data)
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

        val data:clientData = clientData(SHARED_DATA.image_byte!!)
//        Log.d("test","${data}")
        service.getResult(data).enqueue(object : Callback<serverData> {
            override fun onResponse(call: Call<serverData>, response: Response<serverData>) {
                Log.d("test","return : ${response.toString()}")
                Log.d("test",response.body()!!.toString())
                setBottomSheet(response.body()!!)
            }
            override fun onFailure(call: Call<serverData>, t: Throwable) {
                Log.d("test","fail: ${t.printStackTrace()}")
            }
        })
    }
    fun saveBitmapToCacheUri(context: Context, bitmap: Bitmap): Uri? {
        val cache_dir = context.cacheDir
        val cache_file = File(cache_dir,"temp.jpg")
        try {
            val outStream = FileOutputStream(cache_file)
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, outStream)
            outStream.flush()
            outStream.close()
        }catch (exc:Exception){
            Log.d("test","${exc}")
            return null
        }
        return Uri.fromFile(cache_file)
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

        USER_DATA.data = data.copy()
        url_string = "http://"+data.IP +":"+ data.PORT.toString()

//        Log.d("test",data.class_dict.toString())
//        Log.d("test",data.ingredients_dict.toString())
//        Log.d("test",data.IP)
//        Log.d("test",data.PORT.toString())
        Log.d("test",data.checklist.toString())
//        Log.d("test",data.checklist["egg"].toString())
    }

}

