//////////////////////////////////////////////////////////////////////////////
// Name:        SVGDocument.h
// Author:      Alex Thuering
// Copyright:   (c) 2005 Alex Thuering
// Licence:     wxWindows licence
// Notes:       generated by generate.py
//////////////////////////////////////////////////////////////////////////////

#ifndef WX_SVG_DOCUMENT_H
#define WX_SVG_DOCUMENT_H

class wxSVGSVGElement;
class wxSVGElement;
class wxSVGCanvas;
class wxProgressDialog;

#include "Document.h"
#include "DocumentEvent.h"
#include "String_wxsvg.h"
#include "SVGRect.h"
#include "SVGMatrix.h"
#include <wx/image.h>

class wxSVGDocument:
  public wxSvgXmlDocument,
  public wxDocumentEvent
{
  protected:
    wxString m_referrer;
    wxString m_domain;
    wxString m_URL;
    wxString m_path;

  public:
    inline const wxString& GetReferrer() const { return m_referrer; }
    inline void SetReferrer(const wxString& n) { m_referrer = n; }

    inline const wxString& GetDomain() const { return m_domain; }
    inline void SetDomain(const wxString& n) { m_domain = n; }

    inline const wxString& GetURL() const { return m_URL; }
    inline void SetURL(const wxString& n) { m_URL = n; }

    inline const wxString& GetPath() const { return m_path; }
    inline void SetPath(const wxString& n) { m_path = n; }

  protected:
    wxSVGCanvas* m_canvas;
    double m_scale;
    double m_scaleY;

    wxSVGMatrix m_screenCTM;

    double m_time;
    double GetDuration(wxSVGElement* parent);
  public:
    wxSVGDocument() { Init(); }
    wxSVGDocument(const wxString& filename, const wxString& encoding = wxT("UTF-8")):
      wxSvgXmlDocument(filename, encoding) { Init(); }
    wxSVGDocument(wxInputStream& stream, const wxString& encoding = wxT("UTF-8")):
      wxSvgXmlDocument(stream, encoding) { Init(); }
    wxSVGDocument(const wxSVGDocument& doc);
    virtual ~wxSVGDocument();

    virtual bool Load(const wxString& filename, const wxString& encoding = wxT("UTF-8"));
    virtual bool Load(wxInputStream& stream, const wxString& encoding = wxT("UTF-8"));

    void Init();
    inline wxSVGCanvas* GetCanvas() { return m_canvas; }
    inline double GetScale() { return m_scale; }
    inline double GetScaleX() { return m_scale; }
    inline double GetScaleY() { return m_scaleY > 0 ? m_scaleY : m_scale; }
    const wxSVGMatrix& GetScreenCTM() { return m_screenCTM; }

    wxString GetTitle();
    void SetTitle(const wxString& n);

    wxSVGSVGElement* GetRootElement() { return (wxSVGSVGElement*) GetRoot(); }
    void SetRootElement(wxSVGSVGElement* n) { SetRoot((wxSvgXmlElement*) n); }

    wxSVGElement* GetElementById(const wxString& id);

    wxSvgXmlElement* CreateElement(const wxString& tagName);
    wxSvgXmlElement* CreateElementNS(const wxString& namespaceURI, const wxString& qualifiedName);

    double GetDuration();
    double GetCurrentTime() { return m_time; }
    void SetCurrentTime(double seconds);

    /** Renders SVG to bitmap image */
    wxImage Render(int width = -1, int height = -1, const wxSVGRect* rect = NULL, bool preserveAspectRatio = true,
									 bool alpha = false, wxProgressDialog* progressDlg = NULL);
    unsigned char* RenderGetRef(int width, int height, const wxSVGRect* rect,
															bool preserveAspectRatio, bool alpha);

    static void ApplyAnimation(wxSVGElement* parent, wxSVGSVGElement* ownerSVGElement);
  private:
      DECLARE_DYNAMIC_CLASS(wxSVGDocument)
};

#endif // WX_SVG_DOCUMENT_H
