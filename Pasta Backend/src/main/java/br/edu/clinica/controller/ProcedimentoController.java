package br.edu.clinica.controller;

import br.edu.clinica.model.Procedimento;
import br.edu.clinica.service.ProcedimentoService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/procedimentos")
public class ProcedimentoController {

    private final ProcedimentoService service;

    public ProcedimentoController(ProcedimentoService service) {
        this.service = service;
    }

    @GetMapping
    public List<Procedimento> listar() {
        return service.listar();
    }

    @PostMapping
    public Procedimento criar(@RequestBody Procedimento p) {
        return service.salvar(p);
    }

    @DeleteMapping("/{id}")
    public void remover(@PathVariable Long id) {
        service.remover(id);
    }
}
