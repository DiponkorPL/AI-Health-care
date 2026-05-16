import java.awt.*;
import javax.swing.*;
import javax.swing.table.*;
import java.awt.event.*;
import java.io.*;

public class RegistrationFrame extends JFrame implements ActionListener {
    private JTextField tfName, tfCgpa, tfSearch;
    private JCheckBox cb1, cb2, cb3, cb4;
    private JButton btSubmit, btExit, btDelete, btSearch;
    private JTable table;
    private DefaultTableModel model;
    private final String FILE_NAME = "students.txt";

    public RegistrationFrame() {
        super("AIUB Course Registration");
        setBounds(600,200,700,500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel panel = new JPanel();
        panel.setLayout(null);
        panel.setBackground(Color.CYAN);

        JLabel lblName = new JLabel("Name:");
        lblName.setBounds(20, 30, 80, 25);
        panel.add(lblName);

        tfName = new JTextField();
        tfName.setBounds(100, 30, 150, 25);
        panel.add(tfName);

        JLabel lblCgpa = new JLabel("CGPA:");
        lblCgpa.setBounds(20, 70, 80, 25);
        panel.add(lblCgpa);

        tfCgpa = new JTextField();
        tfCgpa.setBounds(100, 70, 150, 25);
        panel.add(tfCgpa);   // ✅ fixed: now added to panel

        JLabel lblCourse = new JLabel("Courses:");
        lblCourse.setBounds(20, 110, 80, 25);
        panel.add(lblCourse);

        cb1 = new JCheckBox("Data Structure");
        cb1.setBounds(100, 110, 150, 25);
        panel.add(cb1);

        cb2 = new JCheckBox("Database");
        cb2.setBounds(100, 140, 150, 25);
        panel.add(cb2);

        cb3 = new JCheckBox("Math4");
        cb3.setBounds(100, 170, 150, 25);
        panel.add(cb3);

        cb4 = new JCheckBox("Circuit");
        cb4.setBounds(100, 200, 150, 25);
        panel.add(cb4);

        String[] cols = {"Name", "CGPA", "Courses"};
        model = new DefaultTableModel(cols, 0);
        table = new JTable(model);
        JScrollPane scroll = new JScrollPane(table);
        scroll.setBounds(300, 30, 370, 250);
        panel.add(scroll);

        btSubmit = new JButton("Submit");

        btSubmit.setBounds(100, 250, 100, 25);
        btSubmit.setBackground(Color.GREEN);  
        btSubmit.setForeground(Color.black);  
        btSubmit.addActionListener(this);
        panel.add(btSubmit);

        btDelete = new JButton("Delete");
        btDelete.setBounds(210, 250, 100, 25);
        btDelete.setBackground(Color.RED);   
        btDelete.setForeground(Color.black); 
        btDelete.addActionListener(this);
        panel.add(btDelete);

        btExit = new JButton("Exit");
        btExit.setBounds(100, 290, 100, 25);
        btExit.setBackground(Color.blue);   
        btExit.setForeground(Color.black);
        btExit.addActionListener(this);
        panel.add(btExit);

        JLabel lblSearch = new JLabel("Search by Name:");
        lblSearch.setBounds(300, 300, 120, 25);
        panel.add(lblSearch);

        tfSearch = new JTextField();
        tfSearch.setBounds(420, 300, 150, 25);
        panel.add(tfSearch);

        btSearch = new JButton("Search");
        btSearch.setBounds(580, 300, 80, 25);
        btSearch.addActionListener(this);
        panel.add(btSearch);

        add(panel);
        loadDataFromFile();
    }

    public void actionPerformed(ActionEvent e) {
        if(e.getSource() == btExit) {
            System.exit(0);
        }
        else if(e.getSource() == btSubmit) {
            String name = tfName.getText();
            String cgpa = tfCgpa.getText();
            String courses = "";

            if(cb1.isSelected()) courses += cb1.getText()+" ";
            if(cb2.isSelected()) courses += cb2.getText()+" ";
            if(cb3.isSelected()) courses += cb3.getText()+" ";
            if(cb4.isSelected()) courses += cb4.getText()+" ";

            if(name.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please enter Name!");
            }
            else if(cgpa.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please enter CGPA!");
            }
            else if(courses.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please select at least one Course!");
            }
            else {
                model.addRow(new Object[]{name, cgpa, courses});
                saveDataToFile(name, cgpa, courses);
                JOptionPane.showMessageDialog(this, "Information saved!");
            }
        }
        else if(e.getSource() == btDelete) {
            int row = table.getSelectedRow();
            if(row >= 0) {
                model.removeRow(row);
                rewriteFile();
                JOptionPane.showMessageDialog(this,"Row deleted!");
            }
            else {
                JOptionPane.showMessageDialog(this,"Select a row or use Search to find data!");
            }
        }
        else if(e.getSource() == btSearch) {
            String searchName = tfSearch.getText();
            boolean found = false;

            if(searchName.isEmpty()) {
                JOptionPane.showMessageDialog(this,"Please enter a name to search!");
            }
            else {
                for(int i=0; i<model.getRowCount(); i++) {
                    String tableName = model.getValueAt(i,0).toString();
                    if(tableName.equalsIgnoreCase(searchName)) {
                        table.setRowSelectionInterval(i,i);
                        found = true;
                        break;
                    }
                }
                if(!found) {
                    JOptionPane.showMessageDialog(this,"No record found with name: "+searchName);
                }
            }
        }
    }

    private void saveDataToFile(String name, String cgpa, String courses) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(FILE_NAME, true))) {
            bw.write(name + "," + cgpa + "," + courses);
            bw.newLine();
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this,"Error saving data!");
        }
    }

    private void loadDataFromFile() {
        try (BufferedReader br = new BufferedReader(new FileReader(FILE_NAME))) {
            String line;
            while((line = br.readLine()) != null) {
                String[] parts = line.split(",");
                if(parts.length == 3) {
                    model.addRow(new Object[]{parts[0], parts[1], parts[2]});
                }
            }
        } catch (IOException ex) {
        }
    }

    private void rewriteFile() {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(FILE_NAME))) {
            for(int i=0; i<model.getRowCount(); i++) {
                String name = model.getValueAt(i,0).toString();
                String cgpa = model.getValueAt(i,1).toString();
                String courses = model.getValueAt(i,2).toString();
                bw.write(name + "," + cgpa + "," + courses);
                bw.newLine();
            }
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this,"Error updating file!");
        }
    }
}
