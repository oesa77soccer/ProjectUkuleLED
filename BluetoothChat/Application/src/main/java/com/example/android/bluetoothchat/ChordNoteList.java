package com.example.android.bluetoothchat;

/**
 * Created by Logan on 4/10/2018.
 */
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;

public class ChordNoteList extends AppCompatActivity {

    String[] nameArray = {"A","A#","B","C","C#","D","D#","E","F","F#","G","G#"};
    ListView listView;
    String cNum = "0";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chord_note_list);
        Intent intent = getIntent();
        cNum = getIntent().getStringExtra("chordNum");

        CustomListAdapter whatever = new CustomListAdapter(this, nameArray);
        listView = (ListView) findViewById(R.id.listviewID);
        listView.setAdapter(whatever);

        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position,
                                    long id) {
                Intent intent = new Intent(ChordNoteList.this, CustomChord.class);
                String message = nameArray[position];
                intent.putExtra("note", message);
                intent.putExtra("chordNum", cNum);
                startActivity(intent);
            }
        });
    }

}
