package com.example.myapplication

import android.opengl.Visibility
import android.os.Bundle
import android.util.Log
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import androidx.fragment.app.Fragment
import com.example.myapplication.databinding.FragmentResultDialogBinding
import com.google.android.material.bottomsheet.BottomSheetBehavior
import com.google.android.material.bottomsheet.BottomSheetBehavior.BottomSheetCallback

class ResultListDialog : Fragment() {

    private lateinit var binding: FragmentResultDialogBinding
    // This property is only valid between onCreateView and
    // onDestroyView.
    private lateinit var behavior: BottomSheetBehavior<LinearLayout>
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        super.onCreateView(inflater, container, savedInstanceState)
        Log.d("test","bottom frag init")

        binding = FragmentResultDialogBinding.inflate(inflater, container, false)

        Log.d("test",container.toString())
        return binding.root
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
//        Log.d("test",binding.infoLayout.toString())

        try {
            //버튼 설정
            binding.floatingActionButton.setImageResource(com.google.android.material.R.drawable.material_ic_menu_arrow_up_black_24dp)
            binding.floatingActionButton.setOnClickListener{
                toggle_bottomsheet()
            }
            behavior = BottomSheetBehavior.from(binding.infoVertical)
            behavior.addBottomSheetCallback(object: BottomSheetCallback(){
                override fun onStateChanged(bottomSheet: View, newState: Int) {
                    when(newState){
                        BottomSheetBehavior.STATE_COLLAPSED ->{
                            Log.d("test","close")
                            binding.floatingActionButton.setImageResource(com.google.android.material.R.drawable.material_ic_menu_arrow_up_black_24dp)
                        }
                        BottomSheetBehavior.STATE_EXPANDED ->{
                            Log.d("test","open")
                            binding.floatingActionButton.setImageResource(com.google.android.material.R.drawable.material_ic_menu_arrow_down_black_24dp)
                        }
                    }
                }

                override fun onSlide(bottomSheet: View, slideOffset: Float) {

                }
            })
            behavior.peekHeight = 90
            activate_bottomsheet()

        }
        catch (exc:Exception){

            Log.d("test",binding.infoStringConstraint.toString())
            Log.d("test",exc.toString())
        }
//        behavior.state = BottomSheetBehavior.STATE_HALF_EXPANDED

    }
    fun toggle_bottomsheet(){
        Log.d("test","toggle")
        when(behavior.state){
            BottomSheetBehavior.STATE_COLLAPSED -> open_bottomsheet()
            BottomSheetBehavior.STATE_EXPANDED -> close_bottomsheet()
        }
    }
    fun close_bottomsheet(){
        behavior.state = BottomSheetBehavior.STATE_COLLAPSED
    }
    fun open_bottomsheet(){
        behavior.state = BottomSheetBehavior.STATE_EXPANDED
    }
    fun activate_bottomsheet(){
        binding.floatingActionButton.isEnabled = true
        behavior.state = BottomSheetBehavior.STATE_EXPANDED
        behavior.isDraggable = true
    }
    fun deactivate_bottomsheet(){
        binding.floatingActionButton.isEnabled = false
        behavior.state = BottomSheetBehavior.STATE_COLLAPSED
        behavior.isDraggable = false
    }
    fun setResult(server_data: serverData){
        binding.floatingActionButton.isEnabled = true
        behavior.state = BottomSheetBehavior.STATE_EXPANDED
        behavior.isDraggable = true


    }

}