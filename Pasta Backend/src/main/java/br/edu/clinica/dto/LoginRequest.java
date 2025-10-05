package br.edu.clinica.dto;

public class LoginRequest {
    private String email;
    private String senha; 
    
    public String getEmail(){ return email; }
    public void setEmail(String e){ this.email = e; }
    public String getSenha(){ return senha; }
    public void setSenha(String s){ this.senha = s; }
}
